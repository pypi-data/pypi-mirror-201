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
"""Classes for concrete implementations Enum and other."""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import hankai.lib


class ServiceFamily(hankai.lib.MemberValue):
    """Orchestrator Service families."""

    AUTOCODING = "autocoding"
    DOCUVISION = "docuvision"


class Service(hankai.lib.MemberValue):
    """Orchestrator Service class."""

    AUTOCODING_1 = "autocoding-1"
    DOCUVISION_1 = "docuvision-1"
    DOCUVISION_2 = "docuvision-2"
    DOCUVISION_3 = "docuvision-3"


class ServiceFamilies:
    """Orchestrator ServiceFamily class. A service member should only be
    assigned to one family."""

    families = {
        ServiceFamily.AUTOCODING: [Service.AUTOCODING_1],
        ServiceFamily.DOCUVISION: [
            Service.DOCUVISION_1,
            Service.DOCUVISION_2,
            Service.DOCUVISION_3,
        ],
    }

    @classmethod
    def family(
        cls,
        service: Service,
    ) -> Optional[ServiceFamily]:
        """Return the family that the service is a member."""
        if service in cls.families[ServiceFamily.AUTOCODING]:
            return ServiceFamily.AUTOCODING
        if service in cls.families[ServiceFamily.DOCUVISION]:
            return ServiceFamily.DOCUVISION

        return None


class ServiceURIs(hankai.lib.MemberValue):
    """Service URI endpoint references."""

    URI = "uri"
    URI_S3_PRESIGNED = "uri_s3_presigned"


class ServiceURI:
    """Service URI endpoints."""

    # pylint: disable=line-too-long
    _service_uri: Dict[ServiceFamily, Dict[ServiceURIs, str]] = {
        ServiceFamily.AUTOCODING: {
            ServiceURIs.URI: "https://services.hank.ai/autocoding/v1/tasks/",
            ServiceURIs.URI_S3_PRESIGNED: "https://services.hank.ai/autocoding/v1/upload-locations/",
        },
        ServiceFamily.DOCUVISION: {
            ServiceURIs.URI: "https://services.hank.ai/docuvision/v1/tasks/",
            ServiceURIs.URI_S3_PRESIGNED: "https://services.hank.ai/docuvision/v1/upload-locations/",
        },
    }

    @classmethod
    def uri(
        cls,
        service_family: ServiceFamily,
    ) -> str:
        """Return Service URI endpoint."""
        if service_family not in cls._service_uri:
            return ""

        return cls._service_uri[service_family][ServiceURIs.URI]

    @classmethod
    def uri_s3_presigned(
        cls,
        service_family: ServiceFamily,
    ) -> str:
        """Return Service URI S3 Presigned endpoint."""
        if service_family not in cls._service_uri:
            return ""

        return cls._service_uri[service_family][ServiceURIs.URI_S3_PRESIGNED]


class SetService(ABC):
    """Orchestrator Service and Set base class."""

    @classmethod
    @abstractmethod
    def supported(cls, service: Service, service_set: Optional[int] = None) -> bool:
        """Supported service."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def features(cls, service_set: int, service: Service) -> Optional[Dict[Any, Any]]:
        """Set service features."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def sets(cls, service: Service) -> List[int]:
        """List of sets by service."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def services_by_set(cls, service_set: int) -> List[Service]:
        """List of set services."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def services_by_set_str(cls, service_set: int) -> List[str]:
        """List of set services as string."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def services(cls) -> List[Service]:
        """List of all services."""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def services_str(cls) -> List[str]:
        """List of all services as string."""
        raise NotImplementedError()


class ResponseState(hankai.lib.MemberValue):
    """ResponseState enum. Case sensitive."""

    IN_PROGRESS = "In-Progress"
    COMPLETED = "Completed"
    ERROR = "Error"


class Model(hankai.lib.MemberValueLower):
    """DocuVision API Models."""

    NONE = "none"
    BASE_MEDREC_ANESTHESIA = "base-medrec-anesthesia"
    UTILITY_BILLS = "utility-bills"
    PURCHASE_ORDERS = "purchase-orders"


class ServiceModel:
    """DocuVision supported service model."""

    _supported_model: Dict[Service, List[Model]] = {
        Service.AUTOCODING_1: [
            Model.NONE,
        ],
        Service.DOCUVISION_1: [
            Model.BASE_MEDREC_ANESTHESIA,
        ],
        Service.DOCUVISION_2: [
            Model.UTILITY_BILLS,
        ],
        Service.DOCUVISION_3: [
            Model.PURCHASE_ORDERS,
        ],
    }

    @classmethod
    def models_str(
        cls,
        service: Service,
    ) -> Optional[List[str]]:
        """Return DocuVision service model string."""
        if service not in cls._supported_model:
            return None

        # pylint: disable=unnecessary-lambda
        return list(map(lambda m: str(m), cls._supported_model[service]))

    @classmethod
    def models(
        cls,
        service: Service,
    ) -> Optional[List[Model]]:
        """Return DocuVision service Model."""
        if service not in cls._supported_model:
            return None

        return cls._supported_model[service]

    @staticmethod
    def supported(
        service: Service,
        model: Model,
    ) -> bool:
        """Identify supported DocuVision service models."""
        if (
            service in ServiceModel._supported_model
            and model in ServiceModel._supported_model[service]
        ):
            return True

        return False


class MimeType:
    """DocuVision supported MimeType."""

    _supported_mime_type: Dict[Service, List[hankai.lib.MimeType]] = {
        Service.AUTOCODING_1: [
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeApplication.JSON),
        ],
        Service.DOCUVISION_1: [
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeApplication.PDF),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.JPG),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.JPEG),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.PNG),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.BMP),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.WEBP),
        ],
        Service.DOCUVISION_2: [
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeApplication.PDF),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.JPG),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.JPEG),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.PNG),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.BMP),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.WEBP),
        ],
        Service.DOCUVISION_3: [
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeApplication.PDF),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.JPG),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.JPEG),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.PNG),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.BMP),
            hankai.lib.MimeType(mime_type=hankai.lib.MimeTypeImage.WEBP),
        ],
    }

    @staticmethod
    def members_str(
        service: Service,
    ) -> Optional[List[str]]:
        """Return DocuVision service mime ext and type string."""
        if service in MimeType._supported_mime_type:
            members: List[str] = []
            for mime_type in MimeType._supported_mime_type[service]:
                members.append(mime_type.ext)
                members.append(str(mime_type))

            return members

        return None

    @staticmethod
    def members(
        service: Service,
    ) -> Optional[List[hankai.lib.MimeType]]:
        """Return DocuVision service mime types."""
        return MimeType._supported_mime_type.get(service)

    @staticmethod
    def supported(
        service: Service,
        mime_type: hankai.lib.MimeType,
    ) -> bool:
        """Identify supported DocuVision service mime types."""
        if (
            service in MimeType._supported_mime_type
            and mime_type in MimeType._supported_mime_type[service]
        ):
            return True

        return False


class ConfidenceInterval(hankai.lib.MemberValue):
    """DocuVision API Confidence Interval."""

    MIN = 0.0
    MAX = 1.0

    @staticmethod
    def normalize(confidence: float) -> float:
        """Return valid confidence."""
        if confidence > ConfidenceInterval.MAX.value:
            return min(confidence, ConfidenceInterval.MAX.value)

        if confidence < ConfidenceInterval.MIN.value:
            return max(confidence, ConfidenceInterval.MIN.value)

        return confidence


@dataclass
class ErrorTrace(Exception):  # pylint: disable=too-many-instance-attributes
    """Custom exception to collect traceback for ErrorTracePickling
    to flatten on pickling.
    """

    message: Optional[str] = None
    tracebacks: Optional[List[str]] = None

    @staticmethod
    def _msg_prefix() -> str:
        return "Message ["

    @staticmethod
    def _msg_suffix() -> str:
        return "]"

    @staticmethod
    def _trc_prefix() -> str:
        return "Tracebacks "

    @staticmethod
    def record_separator() -> str:
        """The error message and tracebacks record separator."""
        return "\u001E"

    def __str__(self) -> str:
        """Return the exception with all available information."""
        error: List[str] = []
        msg_prefix = ErrorTrace._msg_prefix()
        msg_suffix = ErrorTrace._msg_suffix()
        trc_prefix = ErrorTrace._trc_prefix()
        rec_sep = ErrorTrace.record_separator()
        if self.message is None:
            if self.tracebacks is None:
                return ""
            error.append("")
            error.append(f"{trc_prefix}{str(self.tracebacks)}")
        else:
            if self.tracebacks is None:
                error.append(f"{msg_prefix}{self.message}{msg_suffix}")
                error.append("")
            else:
                error.append(f"{msg_prefix}{self.message}]")
                error.append(f"{trc_prefix}{str(self.tracebacks)}")

        return rec_sep.join(error)

    @staticmethod
    def unpicklable(error: Optional[str]) -> Optional[ErrorTrace]:
        """Set the DocuVisionResponseDocument fields from the message.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if error is None:
            return None

        msg_pre_esc = re.escape(ErrorTrace._msg_prefix())
        msg_suf_esc = re.escape(ErrorTrace._msg_suffix())
        trc_pre_esc = re.escape(ErrorTrace._trc_prefix())
        rec_sep = ErrorTrace.record_separator()

        oerror = ErrorTrace()

        message, tracebacks = error.split(rec_sep)
        if message:
            match = re.search(rf"^{msg_pre_esc}(.+){msg_suf_esc}", message)
            if match and match.group(1):
                oerror.message = match.group(1)

        if tracebacks:
            match = re.search(rf"^{trc_pre_esc}(.+)$", tracebacks)
            if match and match.group(1):
                oerror.tracebacks = hankai.lib.Util.objectify(
                    value=match.group(1), type_hint=list
                )

        return oerror
