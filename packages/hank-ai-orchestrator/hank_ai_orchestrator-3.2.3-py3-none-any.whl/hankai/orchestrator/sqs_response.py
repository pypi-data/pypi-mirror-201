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
"""Classes for Orchestrator AWS SQS Response message
serialization/de-serialization.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

import jsonpickle  # type: ignore[import]
import pendulum
from pendulum.datetime import DateTime

import hankai.lib

from .enum_other import ErrorTrace, ResponseState
from .jsonpickle import (
    DateTimePickling,
    EncodingPickling,
    EnumPickling,
    ErrorTracePickling,
    JsonpickleHandler,
)


@dataclass  # type: ignore[misc] # https://github.com/python/mypy/issues/5374
class SQSResponseMessage(ABC):  # pylint: disable=too-many-instance-attributes
    """OrchestratorSQSResponse message."""

    id: Optional[int] = None  # pylint: disable=invalid-name
    name: Optional[str] = None
    state: Optional[ResponseState] = None
    status: Optional[str] = None
    error: Optional[ErrorTrace] = None
    result: Optional[Any] = None
    metadata: Optional[SQSResponseMetadata] = None
    statistics: Optional[SQSResponseStatistic] = None

    @abstractmethod
    def redacted(self) -> SQSResponseMessage:
        """RedactString items that may contain PHI or would pollute the log."""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def jsonpickle_handlers() -> List[JsonpickleHandler]:
        """Jsonpickle handlers for registering when unpicklable False."""
        raise NotImplementedError()

    @abstractmethod
    def validate(self) -> List[str]:
        """Validate the fields."""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def unpicklable(message: Dict[str, Any]) -> SQSResponseMessage:
        """Set the SQSResponseMessage fields from the message.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def unpickle(
        message: Union[Dict[str, Any], str],
        redacted: bool = False,
        jsonpickle_decode_classes: Optional[Set[type]] = None,
    ) -> SQSResponseMessage:
        """Unpickle message non-destructively to SQSResponseMessage."""
        raise NotImplementedError()

    # pylint: disable=too-many-arguments
    def pickle(
        self,
        unpicklable: bool = False,
        redacted: bool = False,
        indent: Optional[int] = None,
        separators: hankai.lib.JsonPickleSeparator = hankai.lib.JsonPickleSeparator.COMPACT,
        jsonpickle_handlers: Optional[List[JsonpickleHandler]] = None,
    ) -> str:
        """Pickle the response message.

        ! NOTE: jsonpickle.encode use_base85=True
        """
        if indent is not None:
            indent = max(indent, 0)

        if unpicklable is False:
            if jsonpickle_handlers is None:
                jsonpickle_handlers = []

            jsonpickle_handlers.append(
                JsonpickleHandler(cls=hankai.lib.Encoding, handler=EncodingPickling)
            )
            jsonpickle_handlers.append(
                JsonpickleHandler(cls=ResponseState, handler=EnumPickling)
            )
            jsonpickle_handlers.append(
                JsonpickleHandler(cls=ErrorTrace, handler=ErrorTracePickling)
            )
            jsonpickle_handlers.append(
                JsonpickleHandler(cls=DateTime, handler=DateTimePickling)
            )
            if jsonpickle_handlers:
                for handler in jsonpickle_handlers:
                    handler.register()

        encode_obj = self
        if redacted:
            encode_obj = self.redacted()

        encoded_str = jsonpickle.encode(
            encode_obj,
            unpicklable=unpicklable,
            use_base85=True,
            indent=indent,
            separators=separators.value,
        )

        # Unregister the handlers to avoid polluting the namespace for
        # other classes.
        if unpicklable is False and jsonpickle_handlers:
            for handler in jsonpickle_handlers:
                handler.unregister()

        if not isinstance(encoded_str, str):
            raise AssertionError(
                "JSON encoding with jsonpickle.encode is not a string."
            )

        return encoded_str


@dataclass
class SQSResponseMetadata:
    """SQSResponseMetadata class."""

    apiVersion: Optional[str] = None  # pylint: disable=invalid-name
    processStartTime: Optional[DateTime] = None  # pylint: disable=invalid-name
    processEndTime: Optional[DateTime] = None  # pylint: disable=invalid-name

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.apiVersion is None:
            invalid.append("Message [SQSResponseMetadata.apiVersion] is required.")
        if self.processStartTime is None:
            invalid.append(
                "Message [SQSResponseMetadata.processStartTime] is required."
            )
        if self.processEndTime is None:
            invalid.append("Message [SQSResponseMetadata.processEndTime] is required.")

        return invalid

    @staticmethod
    def unpicklable(
        metadata: Optional[Dict[str, Any]]
    ) -> Optional[SQSResponseMetadata]:
        """Set the DocuVisionResponseDocument fields from message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if metadata is None:
            return None

        res_metadata = SQSResponseMetadata()
        res_metadata.apiVersion = metadata.get("apiVersion")
        start_time = metadata.get("processStartTime")
        if start_time is not None:
            start_dt = pendulum.parse(start_time)
            if not isinstance(start_dt, DateTime):
                raise AssertionError(
                    f"Attribute [processStartTime={start_time}] could not be "
                    "parsed to pendulum.DateTime."
                )
            res_metadata.processStartTime = start_dt
        end_time = metadata.get("processEndTime")
        if end_time is not None:
            end_dt = pendulum.parse(end_time)
            if not isinstance(end_dt, DateTime):
                raise AssertionError(
                    f"Attribute [processEndTime={end_time}] could not be "
                    "parsed to pendulum.DateTime."
                )
            res_metadata.processEndTime = end_dt

        return res_metadata


@dataclass
class SQSResponseStatistic:  # pylint: disable=invalid-name
    """SQSResponseStatistic class."""

    processDurationSeconds: Optional[float] = None

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.processDurationSeconds is None:
            invalid.append(
                "Message [SQSResponseStatistic.processDurationSeconds] is required."
            )

        return invalid

    @staticmethod
    def unpicklable(
        statistics: Optional[Dict[str, Any]]
    ) -> Optional[SQSResponseStatistic]:
        """Set the DocuVisionResponseDocument fields from message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if statistics is None:
            return None

        res_statistics = SQSResponseStatistic()
        res_statistics.processDurationSeconds = statistics.get("processDurationSeconds")

        return res_statistics
