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
"""Classes for Orchestrator AWS SQS Request and Response message jsonpickle
serialization/de-serialization.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

import jsonpickle  # type: ignore[import]
from pendulum.datetime import DateTime

import hankai.lib

from .enum_other import ErrorTrace


class EnumPickling(jsonpickle.handlers.BaseHandler):
    """Handle Enum for jsonpickle."""

    def restore(self, obj) -> Any:
        """Restore."""

    def flatten(self, obj: Enum, data) -> Any:
        """Flatten."""
        return str(obj)


class DateTimePickling(jsonpickle.handlers.BaseHandler):
    """Handle DateTime for jsonpickle."""

    def restore(self, obj) -> Any:
        """Restore."""

    def flatten(self, obj: DateTime, data) -> str:
        """Flatten."""
        return str(obj)


class EncodingPickling(jsonpickle.handlers.BaseHandler):
    """Handle Encoding for jsonpickle."""

    def restore(self, obj) -> Any:
        """Restore."""

    def flatten(self, obj: hankai.lib.Encoding, data) -> Any:
        """Flatten."""
        return obj.__str__()


class ErrorTracePickling(jsonpickle.handlers.BaseHandler):
    """Handle Exception for jsonpickle. Return the exception including the
    traceback information.
    """

    def restore(self, obj) -> Any:
        """Restore."""

    def flatten(self, obj: ErrorTrace, data) -> str:
        """Flatten."""
        return obj.__str__()


@dataclass
class JsonpickleHandler:
    """Class for Jsonpickle handler."""

    cls: type
    handler: type
    base: bool = False

    def register(self) -> None:
        """Register the handler with jsonpickle.handlers.registry.register."""
        jsonpickle.handlers.registry.register(
            self.cls, handler=self.handler, base=self.base
        )

    def unregister(self) -> None:
        """UnRegister the handler with jsonpickle.handlers.registry.register."""
        jsonpickle.handlers.registry.unregister(self.cls)
