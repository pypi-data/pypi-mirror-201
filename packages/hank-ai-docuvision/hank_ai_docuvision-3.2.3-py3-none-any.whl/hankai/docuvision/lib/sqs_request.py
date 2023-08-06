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
"""Classes for DocuVision AWS SQS Request and Response message
serialization/de-serialization."""
from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

import jsonpickle  # type: ignore[import]

import hankai.lib
import hankai.orchestrator

from .enum_other import SetService


# pylint: disable=invalid-name disable=too-many-instance-attributes
@dataclass
class RequestDocument:
    """RequestDocument class."""

    name: Optional[str] = None
    mimeType: Optional[hankai.lib.MimeType] = None
    sizeBytes: Optional[int] = None
    data: Optional[str] = None
    dataType: Optional[str] = None
    md5Sum: Optional[str] = None
    encodingType: Optional[hankai.lib.Encoding] = None
    model: Optional[hankai.orchestrator.Model] = None
    confidenceInterval: Optional[float] = None
    isPerformOCR: Optional[bool] = None
    dataKey: Optional[str] = None

    # pylint: disable=too-many-branches
    def validate(
        self,
        service: hankai.orchestrator.Service,
        is_api_response: bool = False,
    ) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.name is None:
            invalid.append("Message [RequestDocument.name] is required.")
        if self.mimeType is None:
            invalid.append("Message [RequestDocument.mimeType] is required.")
        elif not hankai.orchestrator.MimeType.supported(
            service=service, mime_type=self.mimeType
        ):
            invalid.append(
                f"Message [RequestDocument.mimeType={self.mimeType}] is not "
                f"supported for service [{service}]."
            )
        if self.sizeBytes is None:
            invalid.append("Message [RequestDocument.sizeBytes] is required.")
        if not is_api_response and self.data is None:
            invalid.append("Message [RequestDocument.data] is required.")
        if self.dataType is None:
            invalid.append("Message [RequestDocument.dataType] is required.")
        if self.md5Sum is None:
            invalid.append("Message [RequestDocument.md5Sum] is required.")
        if self.encodingType is None:
            invalid.append("Message [RequestDocument.encodingType] is required.")
        if self.model is None:
            invalid.append("Message [RequestDocument.model] is required.")
        elif not hankai.orchestrator.ServiceModel.supported(
            service=service, model=self.model
        ):
            invalid.append(
                f"Message [RequestDocument.model={self.model}] is not supported "
                f"for service [{service}]."
            )
        if self.confidenceInterval is None:
            invalid.append("Message [RequestDocument.confidenceInterval] is required.")
        elif (
            self.confidenceInterval < hankai.orchestrator.ConfidenceInterval.MIN.value
            or self.confidenceInterval
            > hankai.orchestrator.ConfidenceInterval.MAX.value
        ):
            invalid.append(
                "Message [RequestDocument.confidenceInterval] minimum "
                f"[{hankai.orchestrator.ConfidenceInterval.MIN}], maximum "
                f"[{hankai.orchestrator.ConfidenceInterval.MAX}]."
            )
        if self.isPerformOCR is None:
            invalid.append("Message [RequestDocument.isPerformOCR] is required.")

        if self.md5Sum and self.data and self.encodingType:
            data_md5sum = hashlib.md5(
                hankai.lib.Util().base_decode(
                    encoded=self.data, base=self.encodingType.base
                )
            )
            if data_md5sum.hexdigest() != self.md5Sum:
                invalid.append(
                    f"Document data [md5Sum={self.md5Sum}] is not "
                    f"equal to the decoded [md5Sum={data_md5sum.hexdigest()}]."
                )

        return invalid

    @staticmethod
    def unpicklable(document: Optional[Dict[str, Any]]) -> Optional[RequestDocument]:
        """Set the RequestDocument fields from the document dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if document is None:
            return None

        req_doc = RequestDocument()
        req_doc.name = document.get("name")
        req_doc.mimeType = hankai.lib.MimeType.member_by(
            member=str(document.get("mimeType"))
        )
        req_doc.sizeBytes = document.get("sizeBytes")
        req_doc.data = document.get("data")
        req_doc.dataType = document.get("dataType")
        req_doc.md5Sum = document.get("md5Sum")
        req_doc.encodingType = hankai.lib.Encoding.unpicklable(
            encoding_type=document.get("encodingType", "")
        )
        req_doc.model = hankai.orchestrator.Model.member_by(
            member=document.get("model", "")
        )
        req_doc.confidenceInterval = document.get("confidenceInterval")
        req_doc.isPerformOCR = document.get("isPerformOCR")
        req_doc.dataKey = document.get("dataKey")

        return req_doc


@dataclass
class DocuVisionSQSRequestMessage(hankai.orchestrator.SQSRequestMessage):
    """DocuVisionSQSRequestMessage message."""

    request: Optional[Request] = None

    def redacted(self) -> DocuVisionSQSRequestMessage:
        """RedactString items that may contain PHI or would pollute the log."""
        req_copy = copy.deepcopy(self)
        if (
            req_copy.request is not None
            and req_copy.request.document is not None
            and req_copy.request.document.data is not None
        ):
            req_copy.request.document.data = hankai.lib.RedactString.STRING.value

        return req_copy

    @staticmethod
    def jsonpickle_handlers() -> List[hankai.orchestrator.JsonpickleHandler]:
        """List of SQSRequestMessage Jsonpickle handlers."""
        jsonpickle_handlers: List[hankai.orchestrator.JsonpickleHandler] = []
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.lib.MimeType, handler=hankai.orchestrator.EnumPickling
            )
        )
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.orchestrator.Service,
                handler=hankai.orchestrator.EnumPickling,
            )
        )
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.orchestrator.Model, handler=hankai.orchestrator.EnumPickling
            )
        )

        return jsonpickle_handlers

    def validate(self, api_client: bool = False) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if not api_client and self.id is None:
            invalid.append("Message [DocuVisionSQSRequestMessage.id] is required.")
        if self.name is None:
            invalid.append("Message [DocuVisionSQSRequestMessage.name] is is required.")
        if self.request is None:
            invalid.append("Message [DocuVisionSQSRequestMessage.request] is required.")
        else:
            invalid.extend(self.request.validate())

        return invalid

    @staticmethod
    def unpicklable(message: Dict[str, Any]) -> DocuVisionSQSRequestMessage:
        """Set the SQSRequestMessage fields from the message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        req_msg = DocuVisionSQSRequestMessage()

        # pylint: disable=attribute-defined-outside-init
        req_msg.id = message.get("id")
        req_msg.name = message.get("name")
        req_msg.request = Request.unpicklable(request=message.get("request"))

        return req_msg

    @staticmethod
    def unpickle(
        message: Union[Dict[str, Any], str],
        redacted: bool = True,
        jsonpickle_decode_classes: Optional[Set[type]] = None,
    ) -> DocuVisionSQSRequestMessage:
        """Unpickle message to DocuVisionSQSResponseMessage."""
        if jsonpickle_decode_classes is None:
            jsonpickle_decode_classes = set()

        if DocuVisionSQSRequestMessage not in jsonpickle_decode_classes:
            jsonpickle_decode_classes.add(DocuVisionSQSRequestMessage)

        request_message: DocuVisionSQSRequestMessage

        msg_str: str = json.dumps(message) if not isinstance(message, str) else message
        msg_dict: Dict[str, Any] = (
            json.loads(message) if isinstance(message, str) else message
        )

        if msg_str and "py/object" in msg_str:
            request_message = jsonpickle.decode(
                msg_str, classes=jsonpickle_decode_classes
            )
            # Pylance thinks unnecessary, but it may not decode to the expected
            # class if the JSON body is not conformant.
            if not isinstance(request_message, DocuVisionSQSRequestMessage):
                raise AssertionError(
                    "Request message could not be decoded to "
                    f"[{DocuVisionSQSRequestMessage}] class."
                )
        else:
            request_message = DocuVisionSQSRequestMessage.unpicklable(message=msg_dict)

        del msg_str
        del msg_dict

        if redacted:
            return request_message.redacted()

        return request_message

    @staticmethod
    def factory(**kwargs: Any) -> DocuVisionSQSRequestMessage:
        """Convenience class to create a SQSRequestMessage."""
        name: str = kwargs["name"]
        request_file: hankai.lib.FileProperties = kwargs["request_file"]
        service: hankai.orchestrator.Service = kwargs["service"]
        data_key: Optional[str] = kwargs.get("data_key")
        req_id: Optional[int] = kwargs.get("req_id")
        model: hankai.orchestrator.Model = kwargs["model"]
        confidence_interval: float = kwargs["confidence_interval"]
        perform_ocr: bool = kwargs["perform_ocr"]
        api_client: bool = kwargs.get("api_client", False)

        request_file.encode_binary()
        request_msg = (
            DocuVisionSQSRequestMessage(  # pylint: disable=unexpected-keyword-arg
                id=req_id,
                name=name,
                request=Request(  # pylint: disable=unexpected-keyword-arg
                    service=service,
                    document=RequestDocument(
                        name=request_file.path,
                        mimeType=request_file.mime_type,
                        sizeBytes=request_file.size_bytes,
                        data=request_file.encoded,
                        dataType="blob",
                        md5Sum=request_file.md5sum,
                        encodingType=request_file.encoding,
                        model=model,
                        confidenceInterval=confidence_interval,
                        isPerformOCR=perform_ocr,
                        dataKey=data_key,
                    ),
                ),
            )
        )

        invalids = request_msg.validate(api_client=api_client)
        if invalids:
            invalid_msg = "\n\t".join(invalids)
            raise ValueError(f"DocuVision request message is invalid:\n\t{invalid_msg}")

        return request_msg


@dataclass
class Request(hankai.orchestrator.Request):
    """Request class."""

    document: Optional[RequestDocument] = None

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.service is None:
            invalid.append("Message [Request.service] is required.")
        if self.document is None:
            invalid.append("Message [Request.document] is required.")
        elif self.service:
            if not SetService.supported(service=self.service):
                invalid.append(
                    f"Message [Request.service={self.service}] is not supported."
                )
            invalid.extend(self.document.validate(service=self.service))

        return invalid

    @staticmethod
    def unpicklable(request: Optional[Dict[str, Any]]) -> Optional[Request]:
        """Set the Request message fields from the request dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if request is None:
            return None

        req = Request()
        req.service = hankai.orchestrator.Service.member_by(
            member=str(request.get("service"))
        )
        req.document = RequestDocument.unpicklable(document=request.get("document"))

        return req
