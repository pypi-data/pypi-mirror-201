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
"""Classes for API Client request message processing."""
from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

import requests  # type: ignore[import]

import hankai.lib

from .api_client import RequestFile
from .api_response import APIResponseMessage
from .enum_other import Service
from .sqs_request import SQSRequestMessage


@dataclass
class APIClientExecutor(ABC):  # pylint: disable=too-many-instance-attributes
    """Post and get executor."""

    service: Service
    token: str
    request_message: SQSRequestMessage
    api_response_message: APIResponseMessage
    request_file: RequestFile
    logenv: hankai.lib.LogEnv
    uri: str
    uri_s3_presigned: str
    unpicklable: bool
    uri_timeout_seconds: Optional[int] = None

    def __post_init__(self) -> None:
        self.request_id: int = -1
        self._headers = {"x-api-key": self.token}

    def get_s3_presigned(self) -> Tuple[str, Dict[str, Any]]:
        """AWS S3 presigned URL for file uploads."""
        resp = None
        resp = requests.request(
            headers=self._headers,
            method="POST",
            url=self.uri_s3_presigned,
            timeout=self.uri_timeout_seconds,
        )
        expected_status = 201
        if resp.status_code != expected_status:
            raise AssertionError(
                "Acquiring presigned AWS S3 information from "
                f"[{self.uri_s3_presigned}] for uploads was unsuccessful. "
                f"Status code [{resp.status_code}]; expecting [{expected_status}]."
            )
        s3_presigned = resp.json()
        if self.logenv.verbosity > 0:
            self.logenv.logger.debug(
                "Presigned URL for upload acquired, status code "
                f"[{resp.status_code}] details:\n{s3_presigned}"
            )

        url: Optional[str] = s3_presigned.get("url")
        fields: Optional[Dict[str, Any]] = s3_presigned.get("fields")

        if url is None or fields is None:
            raise AssertionError(
                "Unable to retrieve AWS S3 presigned [url] or [fields] from "
                "response."
            )

        if self.logenv.verbosity > 0:
            self.logenv.logger.debug(
                "AWS S3 presigned [url={}], fields [fields={}].",
                url,
                fields,
            )

        return (url, fields)

    def post_file_s3_presigned(self) -> None:
        """Post request file to AWS S3 presigned and set [dataKey]."""
        if self.request_message.request is None:
            raise AssertionError("Request message [request] is required.")

        if self.request_file.properties.encoded is None:
            raise AssertionError("Request file [encoded] is required.")

        s3_url, s3_fields = self.get_s3_presigned()

        self.request_message.request.dataKey = s3_fields.get("key")
        if not self.request_message.request.dataKey:
            raise AssertionError("Request message [dataKey] is required.")

        self.logenv.logger.debug(
            "POST request file [{}] to AWS S3 presigned URL [{}].",
            self.request_file.properties.canonical_path,
            s3_url,
        )

        resp = requests.post(
            headers=self._headers,
            url=s3_url,
            data=s3_fields,
            files={"file": self.request_file.properties.encoded},
            timeout=self.uri_timeout_seconds,
        )
        expected_status = 204
        if resp.status_code != expected_status:
            raise AssertionError(
                f"POST request file [{self.request_file.properties.path}] at presigned "
                f"AWS S3 URL [{s3_url}]. Status code "
                f"[{resp.status_code}]; expecting [{expected_status}]."
            )

    def post_request(self) -> APIResponseMessage:
        """Post request to Orchestrator API Gateway. Upload to AWS S3 for
        file data that exceeds the threshold bytes.
        """
        resp = requests.request(
            headers=self._headers,
            method="POST",
            url=self.uri,
            data=self.request_message.pickle(
                unpicklable=self.unpicklable,
                jsonpickle_handlers=self.request_message.jsonpickle_handlers(),
            ),
            timeout=self.uri_timeout_seconds,
        )
        expected_status = 200
        if resp.status_code != expected_status:
            raise AssertionError(
                f"POST of request message [{self.request_message.name}] at "
                f"[{self.uri}] was unsuccessful. Status code "
                f"[{resp.status_code}]; expecting [{expected_status}]."
            )

        response_message: APIResponseMessage = self.api_response_message.unpickle(
            message=resp.json(),
            redacted=False,
            jsonpickle_decode_classes={type(self.api_response_message)},
        )

        if self.logenv.verbosity > 0:
            self.logenv.logger.debug(
                "POST request Response message:\n{}",
                response_message.pickle(
                    unpicklable=self.unpicklable,
                    redacted=True,
                    indent=2,
                    jsonpickle_handlers=response_message.jsonpickle_handlers(),
                ),
            )

        if response_message.id is None:
            raise AssertionError(
                f"Request message name [{self.request_message.name}] has no "
                "response id."
            )

        self.request_id = response_message.id

        return response_message

    def get_response(self) -> Optional[APIResponseMessage]:
        """Orchestrator get request."""
        resp = requests.request(
            headers=self._headers,
            method="GET",
            url=f"{self.uri}{self.request_id}",
        )
        expected_status = 200
        if resp.status_code != expected_status:
            self.logenv.logger.debug(
                f"GET for request message id [{self.request_id}] at "
                f"[{self.uri}] was unsuccessful. Status code "
                f"[{resp.status_code}]; expecting [{expected_status}]."
            )
            return None

        response_message: APIResponseMessage = self.api_response_message.unpickle(
            message=resp.json(),
            redacted=False,
            jsonpickle_decode_classes={type(self.api_response_message)},
        )

        return response_message
