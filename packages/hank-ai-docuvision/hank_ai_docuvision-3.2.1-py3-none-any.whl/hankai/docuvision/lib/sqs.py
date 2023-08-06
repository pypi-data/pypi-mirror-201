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
"""Classes for DocuVision SQS Request and Response message
serialization/de-serialization.
"""
from __future__ import annotations

import hankai.orchestrator

from .sqs_request import DocuVisionSQSRequestMessage
from .sqs_response import DocuVisionSQSResponseMessage, ResponseDocument


class DocuVisionSQSMessageCopy(hankai.orchestrator.SQSMessageCopy):
    """Convenience class to copy common fields from one message type to another."""

    @staticmethod
    def request_to_response(
        request: hankai.orchestrator.SQSRequestMessage,
        response: hankai.orchestrator.SQSResponseMessage,
    ) -> None:
        """Copy request message fields to response message fields."""
        if not isinstance(request, DocuVisionSQSRequestMessage):
            raise AssertionError(
                "Argument [request] must be DocuVIsionSQSRequestMessage."
            )
        if not isinstance(response, DocuVisionSQSResponseMessage):
            raise AssertionError(
                "Argument [response] must be DocuVisionSQSResponseMessage"
            )
        response.id = request.id
        response.name = request.name

        if request.request:
            response.service = request.request.service
            if request.request.document:
                response.processedDocument = ResponseDocument()

            if request.request.document and response.processedDocument:
                # No deep copy required as all of these fields are immutable types.
                # If future immutable fields are included, it may be wise to do
                # a deep copy of them.
                response.processedDocument.name = request.request.document.name
                response.processedDocument.mimeType = request.request.document.mimeType
                response.processedDocument.sizeBytes = (
                    request.request.document.sizeBytes
                )
                response.processedDocument.dataType = request.request.document.dataType
                response.processedDocument.md5Sum = request.request.document.md5Sum
                response.processedDocument.encodingType = (
                    request.request.document.encodingType
                )
                response.processedDocument.model = request.request.document.model
                response.processedDocument.confidenceInterval = (
                    request.request.document.confidenceInterval
                )
                response.processedDocument.isPerformOCR = (
                    request.request.document.isPerformOCR
                )
                response.processedDocument.dataKey = request.request.document.dataKey
