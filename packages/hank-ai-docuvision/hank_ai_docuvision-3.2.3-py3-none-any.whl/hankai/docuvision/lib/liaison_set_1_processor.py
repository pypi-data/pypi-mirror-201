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
"""Classes for DocuVision1LiaisonProcessor request message processing."""
import json
import os
import time
from dataclasses import dataclass
from typing import Optional, Type

import requests  # type: ignore

import hankai.aws
import hankai.lib
import hankai.orchestrator

from .sqs import DocuVisionSQSMessageCopy
from .sqs_request import DocuVisionSQSRequestMessage, RequestDocument
from .sqs_response import DocuVisionSQSResponseMessage, ResponseDocument


class LiaisonSet1ProcessorEnv(hankai.lib.EnvEnum):
    """LiaisonSet1Processor EnvEnum for hankai.docuvision.Processor."""

    HANK_DOCUVISION_LIAISON_PROCESSOR_API_VERSION = "api_version"
    HANK_DOCUVISION_LIAISON_PROCESSOR_URL = "url"
    HANK_DOCUVISION_LIAISON_PROCESSOR_TIMEOUT_SECONDS = "timeout_seconds"
    HANK_DOCUVISION_LIAISON_PROCESSOR_READY_URL = "ready_url"
    HANK_DOCUVISION_LIAISON_PROCESSOR_READY_WAIT_SECONDS = "ready_wait_seconds"
    HANK_DOCUVISION_LIAISON_PROCESSOR_READY_FLAG_PATH = "ready_flag_path"


# pylint: disable=too-many-ancestors,too-many-instance-attributes
@dataclass
class LiaisonSet1Processor(hankai.orchestrator.LiaisonProcessor):
    """LiaisonProcessor class which awaits the DocuVision set 1
    service being ready/available and sends a response for the processed request.
    The read_flag_path is set by the DocuVision set 1 application. To set
    other ENV for SimpleQueueService see
    hankai.aws.resource.sqs.SimpleQueueServiceEnv.

    https://github.com/hank-ai/docuvision/blob/main/flaskapp/src/app.py
    """

    service: hankai.orchestrator.Service
    logenv: hankai.lib.LogEnv
    api_version: str = "1.0.1"
    url: str = f"http://127.0.0.1:8080/predict/{api_version}/"
    timeout_seconds: int = 600
    ready_url: str = "http://127.0.0.1:8080/"
    ready_wait_seconds: int = 90
    ready_flag_path: str = "/tmp/docuvision-ready"
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        self.timeout_seconds = max(self.timeout_seconds, 1)
        self.ready_wait_seconds = max(self.ready_wait_seconds, 1)

    def is_ready(self) -> bool:
        """Wait for gunicorn/app DocuVision set 1 service ready file flag.

        https://github.com/hank-ai/docuvision/blob/main/flaskapp/src/app.py
        """
        is_ready = False
        self.logenv.logger.info(
            "Waiting [{}] seconds for DocuVision service [{}] processor to become "
            "ready.",
            self.ready_wait_seconds,
            self.service,
        )
        wait_cnt = 0
        while wait_cnt < self.ready_wait_seconds:
            time.sleep(1)
            ready = os.path.isfile(self.ready_flag_path)
            if ready:
                response = requests.get(
                    self.ready_url,
                    timeout=self.timeout_seconds,
                )
                if response.status_code != 200:
                    self.logenv.logger.critical(
                        "Response from DocuVision Service [{}] test URL [{}] "
                        "response status code [{}] is not 200.",
                        self.service,
                        self.ready_url,
                        response.status_code,
                    )
                else:
                    is_ready = True
                    break

            wait_cnt += 1

        if is_ready:
            self.logenv.logger.info(
                "DocuVision service [{}] processor is ready to receive requests.",
                self.service,
            )
        else:
            self.logenv.logger.critical(
                "DocuVision service [{}] processor [ready_wait_seconds={}] expired "
                "and the processor is not ready.",
                self.service,
                self.ready_wait_seconds,
            )

        return is_ready

    # pylint: disable=too-many-branches disable=too-many-statements
    def _docuvision_request(
        self,
        document: RequestDocument,
        response: DocuVisionSQSResponseMessage,
    ) -> None:
        """Send the document data to DocuVision set 1 service for processing and
        returning a prepared response message object.
        """
        if not response:
            return
        if document is None or not document.data:
            response.state = hankai.orchestrator.ResponseState.ERROR
            response.error = hankai.orchestrator.ErrorTrace(
                "Document [data] is empty. It is required.", None
            )

        # Set HTTP Requests POST arguments
        json_request = {
            "model": str(document.model),
            "cinterval": document.confidenceInterval,
            "ocr": "1" if document.isPerformOCR else "0",
            "fileType": str(document.mimeType),
            "data": document.data,
            "encodeBase": document.encodingType.base.value
            if document.encodingType and document.encodingType.base
            else None,
        }

        # Send the POST request.
        request_response = requests.post(
            self.url,
            json=json_request,
            timeout=self.timeout_seconds,
        )

        if request_response.status_code != 200:
            response.state = hankai.orchestrator.ResponseState.ERROR
            response.error = hankai.orchestrator.ErrorTrace(
                f"Processor return status [{request_response.status_code}]; "
                f"expecting [200]. Reason: {request_response.reason}",
                None,
            )
            self.logenv.logger.error(
                "Processor URL [{}] response status code "
                "[{}]; expecting [200]. Reason:\n{}",
                self.service,
                self.url,
                request_response.status_code,
                request_response.reason,
            )
        else:
            response.state = hankai.orchestrator.ResponseState.COMPLETED
            response.result = request_response.json()

    def init_response(
        self,
        request: hankai.orchestrator.SQSRequestMessage,
    ) -> DocuVisionSQSResponseMessage:
        """Initialize the response message based on the request message."""
        if not isinstance(request, DocuVisionSQSRequestMessage):
            raise AssertionError(
                "Argument [request] must be DocuVIsionSQSRequestMessage."
            )
        response = DocuVisionSQSResponseMessage()
        response.processedDocument = ResponseDocument()
        response.metadata = hankai.orchestrator.SQSResponseMetadata()
        response.statistics = hankai.orchestrator.SQSResponseStatistic()
        response.state = hankai.orchestrator.ResponseState.IN_PROGRESS

        response.id = request.id
        response.name = request.name
        response.metadata.apiVersion = self.api_version

        return response

    def process_request(
        self,
        request: hankai.orchestrator.SQSRequestMessage,
        response: hankai.orchestrator.SQSResponseMessage,
    ) -> None:
        """Consumer function for DocuVision set 1 service AWS SQS requests queue.
        Processes message body delivery PDF data to the DocuVision set 1 service
        HTTP API. Results are sent to the DocuVision set 1 service AWS SQS responses
        queue.

        ! NOTE: This is primarily a Callable reference method for
        LiaisonWorkers. Other use cases have not been tested.

        https://docs.aws.amazon.com/SimpleQueueService/latest/SQSDeveloperGuide/using-messagegroupid-property.html
        """
        if not isinstance(request, DocuVisionSQSRequestMessage):
            raise AssertionError(
                "Argument [request] must be DocuVisionSQSRequestMessage"
            )
        if not isinstance(response, DocuVisionSQSResponseMessage):
            raise AssertionError(
                "Argument [response] must be DocuVisionSQSResponseMessage"
            )
        DocuVisionSQSMessageCopy.request_to_response(request=request, response=response)

        if (  # pylint: disable=too-many-boolean-expressions
            not request.request
            or not request.request.document
            or not response
            or not response.processedDocument
            or not response.metadata
            or not response.statistics
        ):
            raise AssertionError(
                "Request and/or response message is missing required fields."
            )

        invalids = request.validate()
        if invalids:
            response.state = hankai.orchestrator.ResponseState.ERROR
            if response.error is None:
                response.error = hankai.orchestrator.ErrorTrace(
                    "Request message is invalid.", invalids
                )

        response.metadata.processStartTime = hankai.lib.Util.date_now()

        if response.state != hankai.orchestrator.ResponseState.ERROR:
            self._docuvision_request(
                document=request.request.document,
                response=response,
            )

        # This service uses and intermediate temporary file and
        # the OriginalDocumentName is a random value since the document
        # data was sent via STDIN. Adjust RESULT OriginalDocumentName to
        # match the actual original file name.
        if response.result is not None:
            # Results are comming in as a string; reify into json.
            results = response.result.get("RESULT", [])
            if results:
                for result in results:
                    result["OriginDocumentName"] = response.processedDocument.name

        # This service results must be sting due to character escapes.
        response.result = json.dumps(
            response.result,
            separators=hankai.lib.JsonPickleSeparator.COMPACT.value,
        )

        response.metadata.processEndTime = hankai.lib.Util.date_now()
        response.statistics.processDurationSeconds = hankai.lib.Util.duration_seconds(
            start=response.metadata.processStartTime,
            end=response.metadata.processEndTime,
        )
