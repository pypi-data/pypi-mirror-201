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
"""Classes for Orchestrator AWS SQS Request message
serialization/de-serialization.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

import jsonpickle  # type: ignore[import]

import hankai.lib

from .enum_other import Service
from .jsonpickle import EncodingPickling, JsonpickleHandler


@dataclass  # type: ignore[misc] # https://github.com/python/mypy/issues/5374
class SQSRequestMessage(ABC):
    """SQSRequestMessage message."""

    id: Optional[int] = None  # pylint: disable=invalid-name
    name: Optional[str] = None
    request: Optional[Request] = None

    @abstractmethod
    def redacted(self) -> SQSRequestMessage:
        """RedactString items that may contain PHI or would pollute the log."""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def jsonpickle_handlers() -> List[JsonpickleHandler]:
        """Jsonpickle handlers for registering when unpicklable False."""
        raise NotImplementedError()

    @abstractmethod
    def validate(self, api_client: bool = False) -> List[str]:
        """Validate the fields."""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def unpicklable(message: Dict[str, Any]) -> SQSRequestMessage:
        """Set the SQSRequestMessage fields from the message.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def factory(**kwargs: Any) -> SQSRequestMessage:
        """Convenience factory for creating the request message."""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def unpickle(
        message: Union[Dict[str, Any], str],
        redacted: bool = False,
        jsonpickle_decode_classes: Optional[Set[type]] = None,
    ) -> SQSRequestMessage:
        """Unpickle message non-destructively to SQSRequestMessage."""
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
        """Pickle the request message.

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


@dataclass  # type: ignore
class Request(ABC):
    """Request class."""

    # pylint: disable=invalid-name
    service: Optional[Service] = None
    dataKey: Optional[str] = None

    @abstractmethod
    def validate(self) -> List[str]:
        """Validate the fields."""
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def unpicklable(request: Optional[Dict[str, Any]]) -> Optional[Request]:
        """Set the Request message fields from the request dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        raise NotImplementedError()
