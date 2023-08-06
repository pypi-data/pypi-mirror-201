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
import os
import shutil
from abc import ABC
from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import ParseResult, urlparse

import hankai.lib

from .enum_other import (
    ErrorTrace,
    ResponseState,
    Service,
    ServiceFamilies,
    ServiceFamily,
    ServiceURI,
)


@dataclass
class RequestFile:  # pylint: disable=too-many-instance-attributes
    """Class to track the request files."""

    properties: hankai.lib.FileProperties
    logenv: hankai.lib.LogEnv
    replace_existing_files: bool = False
    processed: bool = False
    processed_relative: bool = True
    processed_directory: str = "processed"
    response_state: Optional[ResponseState] = None
    response_error: Optional[ErrorTrace] = None
    responses_relative: bool = True
    responses_directory: str = "responses"
    responses_extension_separator: Optional[str] = "."
    responses: List[hankai.lib.FileProperties] = field(default_factory=list)

    def __post_init__(self) -> None:
        self._response_id: Optional[int] = None

        relpath: Optional[str] = None
        if self.processed_relative or self.responses_relative:
            relpath = os.path.relpath(
                self.properties.directory,
                self.properties.source_path,
            )
            if relpath == ".":
                relpath = None

        self._set_processed_dir(relpath=relpath)
        self._set_responses_dir(relpath=relpath)

    def _set_processed_dir(self, relpath: Optional[str] = None) -> None:
        """Set the processed directory."""
        if self.processed_relative:
            if os.path.isabs(self.processed_directory):
                if relpath is not None:
                    self.processed_directory = os.path.join(
                        self.processed_directory,
                        relpath,
                    )
            else:
                self.processed_directory = os.path.join(
                    self.properties.directory,
                    self.processed_directory,
                )
        else:
            abspath = os.path.abspath(self.processed_directory)
            self.processed_directory = abspath

    def _set_responses_dir(self, relpath: Optional[str] = None) -> None:
        """Set the responses directory."""
        if self.responses_relative:
            if os.path.isabs(self.responses_directory):
                if relpath is not None:
                    self.responses_directory = os.path.join(
                        self.responses_directory,
                        relpath,
                    )
            else:
                self.responses_directory = os.path.join(
                    self.properties.directory,
                    self.responses_directory,
                )
        else:
            abspath = os.path.abspath(self.responses_directory)
            self.responses_directory = abspath

        if os.path.exists(self.processed_directory):
            if not os.path.isdir(self.processed_directory):
                raise AssertionError(
                    f"Processed directory [{self.processed_directory}] "
                    "exists and is not a directory."
                )

        if os.path.exists(self.responses_directory):
            if not os.path.isdir(self.responses_directory):
                raise AssertionError(
                    f"Responses directory [{self.responses_directory}] "
                    "exists and is not a directory."
                )

    def set_response_job_id(self, response_id: Optional[int]) -> None:
        """Set the request's response job id."""
        self._response_id = response_id

    def get_response_job_id(self) -> Optional[int]:
        """Get the request's response job id."""
        return self._response_id

    def processed_destination(self) -> str:
        """Return the processed destination path."""
        return os.path.join(self.processed_directory, self.properties.name)

    def add_response(
        self, encoded: str, extension: Optional[hankai.lib.MimeType] = None
    ) -> None:
        """Add a response file to the collection of responses created from a
        processed request. Usually it will just be the JSON response output.
        However, there may be additional response outputs as would be the case
        if a transformer is used. e.g. CSV transformer.
        """
        separator = ""
        if self.responses_extension_separator is not None:
            separator = self.responses_extension_separator

        response_file_path = os.path.join(
            self.responses_directory,
            separator.join(
                (
                    self.properties.name_excl_extension,
                    extension.ext if extension is not None else "",
                )
            ),
        )
        response_file = hankai.lib.FileProperties(
            path=response_file_path,
            source_path=self.properties.source_path,
        )
        response_file.encoded = encoded

        self.responses.append(response_file)

    def reconcile(self) -> None:
        """Move request file to processed directory. Save the responses."""
        # Save responses first;
        for response in self.responses:
            hankai.lib.Sys.write_file(
                file=response.canonical_path,
                data=response.encoded if response.encoded is not None else b"",
                replace_existing=self.replace_existing_files,
                make_missing_dirs=True,
            )
            self.logenv.logger.debug(
                "Posted request file [{}] job [id={}] saved response result [{}].",
                self.properties.canonical_path,
                self.get_response_job_id(),
                response.path,
            )
            del response.encoded

        # Move request file
        if not os.path.exists(self.processed_directory):
            os.makedirs(self.processed_directory)

        request_path: str = os.path.join(self.processed_directory, self.properties.name)
        if os.path.exists(path=request_path):
            if self.replace_existing_files:
                os.remove(path=request_path)
            else:
                raise AssertionError(
                    f"Processed destination path [{request_path}] exists."
                )

        shutil.move(src=self.properties.canonical_path, dst=request_path)
        self.logenv.logger.debug(
            "Posted request file [{}] job [id={}] moved to [{}].",
            self.properties.canonical_path,
            self.get_response_job_id(),
            request_path,
        )
        del self.properties.encoded


class APIClientDefault:
    """API Client defaults."""

    size_bytes_s3_presigned_threshold: int = 250000
    timeout_minutes: Optional[int] = None
    uri_timeout_seconds: Optional[int] = None


@dataclass
class APIClient(ABC):  # pylint: disable=too-many-instance-attributes
    """Post and get."""

    service: Service
    token: str
    version: str
    logenv: hankai.lib.LogEnv = hankai.lib.LogEnv(env=hankai.lib.LogEnvEnv)
    backoff: hankai.lib.Backoff = hankai.lib.Backoff(env=hankai.lib.BackoffEnv)
    uri: Optional[str] = None
    uri_s3_presigned: Optional[str] = None
    # https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html
    # Max bytes: 262144, set lower as a safety margin.
    size_bytes_s3_presigned_threshold: int = (
        APIClientDefault.size_bytes_s3_presigned_threshold
    )
    name: Optional[str] = None
    unpicklable: bool = True
    timeout_minutes: Optional[int] = APIClientDefault.timeout_minutes
    uri_timeout_seconds: Optional[int] = APIClientDefault.uri_timeout_seconds
    log_format: str = (
        "{time:!UTC} | <level>{level: <8}</level> | {level.icon} | "
        "<level>{message}</level> | "
        "<light-blue>{thread.name}</light-blue> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>"
    )

    def __post_init__(self) -> None:
        self.logenv.set_log_format(pattern=self.log_format)

        self._service_check()

        if self.timeout_minutes is not None:
            self.timeout_minutes = max(self.timeout_minutes, 1)
        if self.uri_timeout_seconds is not None:
            self.uri_timeout_seconds = max(self.uri_timeout_seconds, 5)

        if self.timeout_minutes is not None:
            self.timeout_minutes = max(self.timeout_minutes, 1)

        self._headers = {"x-api-key": self.token}

    def _service_check(self) -> None:  # pylint: disable=too-many-branches
        """Check the combination of Defaults, CLI and ENV by service."""
        # Configure based on the service family.
        if ServiceFamilies.family(service=self.service) is ServiceFamily.AUTOCODING:
            # URIs.
            if not self.uri:
                self.uri = ServiceURI.uri(service_family=ServiceFamily.AUTOCODING)

            if not self.uri_s3_presigned:
                self.uri_s3_presigned = ServiceURI.uri_s3_presigned(
                    service_family=ServiceFamily.AUTOCODING
                )

        elif ServiceFamilies.family(service=self.service) is ServiceFamily.DOCUVISION:
            # URIs.
            if not self.uri:
                self.uri = ServiceURI.uri(service_family=ServiceFamily.DOCUVISION)
            if not self.uri_s3_presigned:
                self.uri_s3_presigned = ServiceURI.uri_s3_presigned(
                    service_family=ServiceFamily.DOCUVISION
                )

        if self.uri is None or self.uri_s3_presigned is None:
            raise ValueError("Argument [uri] and [uri_s3_presigned] are required.")

        APIClient.uri_validate(self.uri)
        APIClient.uri_validate(self.uri_s3_presigned)

    @staticmethod
    def uri_validate(uri: str) -> None:
        """URI validator."""
        uri_parsed: ParseResult = urlparse(url=uri)
        if not uri_parsed.scheme or uri_parsed.scheme != "https":
            raise ValueError("Argument [uri] scheme must be [https]")
        if not uri_parsed.netloc:
            raise ValueError("Argument [uri] net location is required.")
