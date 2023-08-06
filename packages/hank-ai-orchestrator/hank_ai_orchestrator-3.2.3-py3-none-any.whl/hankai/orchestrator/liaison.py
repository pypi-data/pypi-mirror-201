#
# MIT License
#
# Copyright © 2022 Hank AI, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
"""Orchestrator liasion to receive AWS SQS Orchestrator request queue messages,
process the data via Orchestrator service and respond with results to the AWS SQS
Orchestrator responses queue.
"""
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass

# from multiprocessing.connection import Connection, Pipe
from typing import Any, List, Optional, Type

import backoff
import jsonpickle  # type: ignore[import]

import hankai.aws
import hankai.lib

from .enum_other import ErrorTrace, ResponseState
from .sqs_request import SQSRequestMessage
from .sqs_response import SQSResponseMessage


class LiaisonProcessor(ABC):
    """Processor class which awaits the Orchestrator service being
    ready/available and sends a response for the processed request. The
    read_flag_path is set by the Orchestrator application. To set other
    ENV for SimpleQueueService see
    hankai.aws.resource.sqs.SimpleQueueServiceEnv.

    ! IMPORTANT: SimpleQueueService ENV supersede is *disabled*.
    """

    @abstractmethod
    def is_ready(self) -> bool:
        """Orchestrator processor is ready."""
        raise NotImplementedError()

    @abstractmethod
    def init_response(
        self,
        request: SQSRequestMessage,
    ) -> SQSResponseMessage:
        """Initialize the response message based on the request message."""
        raise NotImplementedError()

    @abstractmethod
    def process_request(
        self,
        request: SQSRequestMessage,
        response: SQSResponseMessage,
    ) -> None:
        """Consumer function for Orchestrator AWS SQS requests queue.
        Processes message body delivery PDF data to the Orchestrator HTTP API.
        Results are sent to the Orchestrator AWS SQS responses queue.

        ! NOTE: This is primarily a Callable reference method for
        LiaisonWorkers. Other use cases have not been tested.

        https://docs.aws.amazon.com/SimpleQueueService/latest/SQSDeveloperGuide/using-messagegroupid-property.html
        """
        raise NotImplementedError()


class LiaisonEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and LiaisonWorkersEnv attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_LIAISON_UNPICKLABLE = "unpicklable"


@dataclass
class Liaison(ABC):  # pylint: disable=too-many-instance-attributes
    """Orchestrator liaison."""

    processor: LiaisonProcessor
    requests_queue: hankai.aws.SimpleQueueService
    request_message: Type[SQSRequestMessage]
    responses_queue: hankai.aws.SimpleQueueService
    response_message: Type[SQSResponseMessage]
    backoff: hankai.lib.Backoff
    logenv: hankai.lib.LogEnv
    unpicklable: bool = True
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        _, self._request_message_class = hankai.lib.Util.class_by_hint(
            type_str=self.request_message.__name__,
            type_hint=self.request_message,
        )

        _, self._response_message_class = hankai.lib.Util.class_by_hint(
            type_str=self.response_message.__name__,
            type_hint=self.response_message,
        )

    def start(  # pylint: disable=too-many-branches, disable=too-many-statements
        self,
    ) -> None:
        """Process AWS SQS requests and execute the callback."""
        self.logenv.logger.info(
            "Orchestrator liaison started [{}] with processor [{}].",
            hankai.lib.Util.date_now(),
            type(self.processor),
        )
        if not self.processor.is_ready():
            raise AssertionError(
                f"Orchestrator liaison processor [{type(self.processor)}] is "
                "not ready."
            )

        self.logenv.logger.info(
            "Orchestrator liaison worker started [{}]",
            hankai.lib.Util.date_now(),
        )

        @backoff.on_predicate(
            backoff.expo,
            lambda x: x is None,
            max_value=self.backoff.max_value_seconds,
            max_time=self.backoff.max_time_seconds,
            jitter=backoff.full_jitter,
            logger=None,
        )
        def _receive_message() -> Optional[List[hankai.aws.SQSMessage]]:
            messages: List[
                hankai.aws.SQSMessage
            ] = self.requests_queue.client_receive_message()

            if not messages:
                if self.logenv.verbosity > 0:
                    self.logenv.logger.info(
                        "Zero messages received from requests queue [{}]; "
                        "triggering backoff.",
                        self.requests_queue.queue_url,
                    )
                return None

            return messages

        while True:
            sqs_messages = _receive_message()
            if sqs_messages is None:
                # This thread is blocked by _inner_receive backoff.
                # messages=None should never occur.
                raise AssertionError("Received request messages [None].")

            self.logenv.logger.debug(
                "Received [{}] request messages.", len(sqs_messages)
            )
            for sqs_message in sqs_messages:

                if not sqs_message.body:
                    raise ValueError("Request message was empty or had no [Body].")

                if sqs_message.receipt_handle is None:
                    raise ValueError("Request message has no [ReceiptHandle].")

                self.logenv.logger.debug(
                    "Received SQSMessage request message:{}",
                    jsonpickle.encode(sqs_message.redacted(), indent=2)
                    if self.logenv.verbosity > 1
                    else "(redacted; verbosity < 2)",
                )

                request_message = self._request_message_class
                response_message = self._response_message_class

                try:
                    request_message = self._request_message_class.unpickle(
                        message=sqs_message.body,
                        redacted=False,
                        jsonpickle_decode_classes={self._request_message_class},
                    )
                    response_message = self.processor.init_response(
                        request=request_message
                    )
                except AssertionError:
                    if not isinstance(response_message, self._response_message_class):
                        response_message = self._response_message_class()
                    response_message.state = ResponseState.ERROR
                    response_message.error = ErrorTrace(
                        message="Request message could not be objectified."
                        "The request message wil not be processed.",
                        tracebacks=hankai.lib.Util.formatted_traceback_exceptions(),
                    )
                    try:
                        # Last ditch effort to get the at least the id and name.
                        # without it the message is useless to the orchestrator.
                        body_json = json.loads(sqs_message.body)
                        response_message.id = body_json.get("id")
                        response_message.name = body_json.get("name")
                    except:  # pylint: disable=bare-except
                        pass

                job_start_time = hankai.lib.Util.date_now()

                self.logenv.logger.debug(
                    "Received request message [message_id={}]:\n{}",
                    sqs_message.message_id,
                    request_message.pickle(
                        unpicklable=self.unpicklable,
                        redacted=True,
                        indent=2,
                        jsonpickle_handlers=request_message.jsonpickle_handlers(),
                    )
                    if self.logenv.verbosity > 1
                    else "(redacted; verbosity < 2)",
                )

                self.logenv.logger.info(
                    "Job request [id={}] processing started [{}].",
                    request_message.id,
                    job_start_time,
                )

                self.processor.process_request(
                    request=request_message,
                    response=response_message,
                )

                sqs_response: Optional[Any] = None

                # Without the id; the message is useless to the orchestrator.
                if response_message.id:
                    sqs_response = self.responses_queue.send_message(
                        message=response_message.pickle(
                            unpicklable=self.unpicklable,
                            jsonpickle_handlers=response_message.jsonpickle_handlers(),
                        )
                    )

                    self.logenv.logger.debug(
                        "Orchestrator response message for job [id={}] "
                        "request message [ReceiptHandle={}] and AWS SQS "
                        "send response:"
                        "\n{}\n::::\n{}",
                        request_message.id,
                        sqs_message.receipt_handle,
                        response_message.pickle(
                            redacted=True,
                            unpicklable=self.unpicklable,
                            indent=2,
                            jsonpickle_handlers=response_message.jsonpickle_handlers(),
                        ),
                        jsonpickle.encode(sqs_response, indent=2)
                        if self.logenv.verbosity > 1
                        else "(redacted; verbosity < 2)",
                    )

                if sqs_response is not None:
                    self.requests_queue.delete_message(
                        receipt_handle=sqs_message.receipt_handle
                    )
                elif not response_message.id:
                    self.logenv.logger.warning(
                        "The Orchestrator response message was not sent "
                        "[id=None]. Request message [ReceiptHandle={}] from "
                        "requests queue [{}] will not be deleted.",
                        sqs_message.receipt_handle,
                        self.requests_queue.queue_url,
                    )
                else:
                    self.logenv.logger.warning(
                        "Orchestrator processing for job [id={}] finished "
                        "with state [{}]. Sending the Orchestrator "
                        "response message did not receive an AWS SQS "
                        "response. Request message [ReceiptHandle={}] from "
                        "requests queue [{}] will not be deleted.",
                        request_message.id,
                        response_message.state,
                        sqs_message.receipt_handle,
                        self.requests_queue.queue_url,
                    )

                job_duration = hankai.lib.Util.elapsed_seconds(start=job_start_time)

                log_message = (
                    f"Job request [id={response_message.id}] processing "
                    f"completed [{hankai.lib.Util.date_now()}] with "
                    f"response state [{response_message.state}]; "
                    f"duration [{job_duration}] seconds."
                )

                if response_message.state == ResponseState.COMPLETED:
                    self.logenv.logger.success(log_message)
                elif response_message.state == ResponseState.ERROR:
                    self.logenv.logger.error(log_message)
                else:
                    self.logenv.logger.warning(log_message)
