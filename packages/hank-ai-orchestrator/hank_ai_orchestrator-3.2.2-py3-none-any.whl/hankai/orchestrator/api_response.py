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
"""Classes for Orchestrator API Response message serialization/de-serialization."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

import jsonpickle  # type: ignore[import]
import pendulum
from pendulum.datetime import DateTime

import hankai.lib

from .enum_other import ErrorTrace, ResponseState, Service
from .jsonpickle import (
    DateTimePickling,
    EncodingPickling,
    EnumPickling,
    ErrorTracePickling,
    JsonpickleHandler,
)


@dataclass  # type: ignore[misc] # https://github.com/python/mypy/issues/5374
class APIResponseMessage(
    ABC
):  # pylint: disable=too-many-instance-attributes,  disable=invalid-name
    """Orchestrator API response message."""

    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    request: Optional[Any] = None
    response: Optional[Any] = None
    state: Optional[ResponseState] = None
    status: Optional[str] = None
    metadata: Optional[APIResponseMetadata] = None
    error: Optional[ErrorTrace] = None

    @abstractmethod
    def redacted(self) -> APIResponseMessage:
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
    def unpicklable(message: Dict[str, Any]) -> APIResponseMessage:
        """Set the APIResponseMessage fields from the message.

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
    ) -> APIResponseMessage:
        """Unpickle message to APIResponseMessage."""
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
class APIResponseMetadata:  # pylint: disable=too-many-instance-attributes, disable=invalid-name
    """APIMetadata class."""

    apiKey: Optional[str] = None
    dataKey: Optional[str] = None
    service: Optional[Service] = None
    metering: Optional[APIResponseMetadataMetering] = None
    timeStamp: Optional[DateTime] = None
    apiVersion: Optional[str] = None
    processStartTime: Optional[DateTime] = None
    processEndTime: Optional[DateTime] = None

    def validate(self) -> List[str]:  # pylint: disable=no-self-use
        """Validate the fields.

        NOTE! No known field requirements. There are no field validations.
        """
        return []

    @staticmethod
    def unpicklable(
        metadata: Optional[Dict[str, Any]]
    ) -> Optional[APIResponseMetadata]:
        """Set the APIResponseMetadata fields from message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if metadata is None:
            return None

        res_metadata = APIResponseMetadata()

        res_metadata.apiKey = metadata.get("apiKey")
        res_metadata.dataKey = metadata.get("dataKey")
        res_metadata.service = Service.member_by(member=str(metadata.get("service")))
        res_metadata.metering = APIResponseMetadataMetering.unpicklable(
            metering=metadata.get("metering")
        )
        time_stamp = metadata.get("timeStamp")
        if time_stamp is not None:
            time_stamp_dt = pendulum.parse(time_stamp)
            if not isinstance(time_stamp_dt, DateTime):
                raise AssertionError(
                    f"Attribute [time_stamp={time_stamp}] could not be "
                    "parsed to pendulum.DateTime."
                )
            res_metadata.timeStamp = time_stamp_dt
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
class APIResponseMetadataMetering:
    """APIMetadataMetering class."""

    total_pages: Optional[int] = None

    def validate(self) -> List[str]:  # pylint: disable=no-self-use
        """Validate the fields.

        NOTE! No known field requirements. There are no field validations.
        """
        return []

    @staticmethod
    def unpicklable(
        metering: Optional[Dict[str, Any]]
    ) -> Optional[APIResponseMetadataMetering]:
        """Set the APIResponseMetadataMetering fields from message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if metering is None:
            return None

        res_mm = APIResponseMetadataMetering()

        res_mm.total_pages = metering.get("total_pages")

        return res_mm
