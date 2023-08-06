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
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

import jsonpickle  # type: ignore[import]

import hankai.lib
import hankai.orchestrator

from .enum_other import SetService


# pylint: disable=too-many-instance-attributes
@dataclass
class DocuVisionSQSResponseMessage(hankai.orchestrator.SQSResponseMessage):
    """DocuVisionSQSResponse message."""

    service: Optional[hankai.orchestrator.Service] = None
    processedDocument: Optional[ResponseDocument] = None  # pylint: disable=invalid-name

    def redacted(self) -> DocuVisionSQSResponseMessage:
        """RedactString items that may contain PHI or would pollute the log."""
        res_copy = copy.deepcopy(self)
        if res_copy.result is not None:
            res_copy.result = hankai.lib.RedactString.STRING.value

        return res_copy

    @staticmethod
    def jsonpickle_handlers() -> List[hankai.orchestrator.JsonpickleHandler]:
        """List of DocuVisionSQSResponseMessage Jsonpickle handlers."""
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

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.id is None:
            invalid.append("Message [DocuVisionSQSResponseMessage.id] is required.")
        if self.name is None:
            invalid.append("Message [DocuVisionSQSResponseMessage.name] is required.")
        if self.service is None:
            invalid.append(
                "Message [DocuVisionSQSResponseMessage.service] is is required."
            )
        if self.state is None:
            invalid.append("Message [DocuVisionSQSResponseMessage.state] is required.")
        if self.result is None:
            invalid.append("Message [DocuVisionSQSResponseMessage.result] is required.")
        if self.metadata is None:
            invalid.append(
                "Message [DocuVisionSQSResponseMessage.metadata] is required."
            )
        if self.statistics is None:
            invalid.append(
                "Message [DocuVisionSQSResponseMessage.statistics] is required."
            )
        if self.processedDocument is None:
            invalid.append(
                "Message [DocuVisionSQSResponseMessage.processedDocument] is "
                "required."
            )
        elif self.service is not None:
            if not SetService.supported(service=self.service):
                invalid.append(
                    "Message [DocuVisionSQSResponseMessage.service] is not supported."
                )
            invalid.extend(self.processedDocument.validate(service=self.service))

        return invalid

    @staticmethod
    def unpicklable(message: Dict[str, Any]) -> DocuVisionSQSResponseMessage:
        """Set the DocuVisionSQSResponseMessage fields from the message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        res_msg = DocuVisionSQSResponseMessage()

        # pylint: disable=attribute-defined-outside-init, disable=invalid-name
        res_msg.id = message.get("id")
        res_msg.name = message.get("name")
        res_msg.service = hankai.orchestrator.Service.member_by(
            member=str(message.get("service"))
        )
        res_msg.state = hankai.orchestrator.ResponseState.member_by(
            str(message.get("state"))
        )
        res_msg.status = message.get("status")
        res_msg.error = hankai.orchestrator.ErrorTrace.unpicklable(
            error=message.get("error")
        )
        res_msg.result = message.get("result")
        res_msg.metadata = hankai.orchestrator.SQSResponseMetadata.unpicklable(
            metadata=message.get("metadata", {})
        )
        res_msg.statistics = hankai.orchestrator.SQSResponseStatistic.unpicklable(
            statistics=message.get("statistics", {})
        )
        res_msg.processedDocument = ResponseDocument.unpicklable(
            document=message.get("processedDocument", {})
        )

        return res_msg

    @staticmethod
    def unpickle(
        message: Union[Dict[str, Any], str],
        redacted: bool = True,
        jsonpickle_decode_classes: Optional[Set[type]] = None,
    ) -> DocuVisionSQSResponseMessage:
        """Unpickle message to DocuVisionSQSResponseMessage."""
        if jsonpickle_decode_classes is None:
            jsonpickle_decode_classes = set()

        if DocuVisionSQSResponseMessage not in jsonpickle_decode_classes:
            jsonpickle_decode_classes.add(DocuVisionSQSResponseMessage)

        response_message: DocuVisionSQSResponseMessage

        msg_str: str = json.dumps(message) if not isinstance(message, str) else message
        msg_dict: Dict[str, Any] = (
            json.loads(message) if isinstance(message, str) else message
        )

        if msg_str and "py/object" in msg_str:
            response_message = jsonpickle.decode(
                msg_str, classes=jsonpickle_decode_classes
            )
            # Pylance thinks unnecessary, but it may not decode to the expected
            # class if the JSON body is not conformant.
            if not isinstance(response_message, DocuVisionSQSResponseMessage):
                raise AssertionError(
                    "Request message could not be decoded to "
                    f"[{DocuVisionSQSResponseMessage}] class."
                )
        else:
            response_message = DocuVisionSQSResponseMessage.unpicklable(
                message=msg_dict
            )

        del msg_str
        del msg_dict

        if redacted:
            return response_message.redacted()

        return response_message


# pylint: disable=invalid-name disable=too-many-instance-attributes
@dataclass
class ResponseDocument:
    """DocuVisionDocument class."""

    name: Optional[str] = None
    mimeType: Optional[hankai.lib.MimeType] = None
    sizeBytes: Optional[int] = None
    dataType: Optional[str] = None
    md5Sum: Optional[str] = None
    encodingType: Optional[hankai.lib.Encoding] = None
    model: Optional[hankai.orchestrator.Model] = None
    confidenceInterval: Optional[float] = None
    isPerformOCR: Optional[bool] = None
    dataKey: Optional[str] = None

    def validate(self, service: hankai.orchestrator.Service) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.name is None:
            invalid.append("Message [ResponseDocument.name] is required.")
        if self.mimeType is None:
            invalid.append("Message [ResponseDocument.mimeType] is required.")
        if self.sizeBytes is None:
            invalid.append("Message [ResponseDocument.sizeBytes] is required.")
        if self.dataType is None:
            invalid.append("Message [ResponseDocument.dataType] is required.")
        if self.md5Sum is None:
            invalid.append("Message [ResponseDocument.md5Sum] is required.")
        if self.encodingType is None:
            invalid.append("Message [ResponseDocument.encodingType] is required.")
        if self.model is None:
            invalid.append("Message [ResponseDocument.model] is required.")
        elif not hankai.orchestrator.ServiceModel.supported(
            service=service, model=self.model
        ):
            invalid.append(
                f"Message [ResponseDocument.model={self.model}] is not supported "
                f"for service [{service}]."
            )
        if self.confidenceInterval is None:
            invalid.append("Message [ResponseDocument.confidenceInterval] is required.")
        if self.isPerformOCR is None:
            invalid.append("Message [ResponseDocument.isPerformOCR] is required.")

        return invalid

    @staticmethod
    def unpicklable(document: Optional[Dict[str, Any]]) -> Optional[ResponseDocument]:
        """Set the ResponseDocument fields from document dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if document is None:
            return None

        res_doc = ResponseDocument()

        res_doc.name = document.get("name")
        res_doc.mimeType = hankai.lib.MimeType.member_by(
            member=str(document.get("mimeType"))
        )
        res_doc.sizeBytes = document.get("sizeBytes")
        res_doc.dataType = document.get("dataType")
        res_doc.md5Sum = document.get("md5Sum")
        res_doc.encodingType = hankai.lib.Encoding.unpicklable(
            encoding_type=document.get("encodingType", "")
        )
        res_doc.model = hankai.orchestrator.Model.member_by(
            member=document.get("model", "")
        )
        res_doc.confidenceInterval = document.get("confidenceInterval")
        res_doc.isPerformOCR = document.get("isPerformOCR")
        res_doc.dataKey = document.get("dataKey")

        return res_doc
