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
"""Classes for DocuVision2LiaisonProcessor request message processing."""
import json
import os
import threading
from dataclasses import dataclass
from typing import Optional, Type

import hankai.aws
import hankai.lib
import hankai.orchestrator

from .sqs import DocuVisionSQSMessageCopy
from .sqs_request import DocuVisionSQSRequestMessage, RequestDocument
from .sqs_response import DocuVisionSQSResponseMessage, ResponseDocument


class LiaisonSet2ProcessorEnv(hankai.lib.EnvEnum):
    """LiaisonSet2Processor EnvEnum for hankai.docuvision.Processor."""

    HANK_DOCUVISION_LIAISON_PROCESSOR_API_VERSION = "api_version"
    HANK_DOCUVISION_LIAISON_PROCESSOR_APP = "app"
    HANK_DOCUVISION_LIAISON_PROCESSOR_OUTPUT_DIRECTORY = "output_dir"


# pylint: disable=too-many-ancestors,too-many-instance-attributes
@dataclass
class LiaisonSet2Processor(hankai.orchestrator.LiaisonProcessor):
    """LiaisonProcessor class which awaits the DocuVision set 2
    service being ready/available and sends a response for the processed request.
    """

    service: hankai.orchestrator.Service
    app: str
    logenv: hankai.lib.LogEnv
    api_version: str = "1.0.1"
    output_dir: str = "/tmp"
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

    def is_ready(self) -> bool:  # pylint: disable=no-self-use
        """DocuVision set 2 service is not a persistent running processor. It
        does not require a lengthy warmup.

        https://github.com/hank-ai/docuvision/blob/main/flaskapp/src/app.py
        """
        if os.path.isfile(self.app) and os.access(self.app, os.X_OK):
            self.logenv.logger.info(
                "DocuVision service [{}] processor is ready to receive requests.",
                self.service,
            )
            return True

        return False

    # pylint: disable=too-many-branches disable=too-many-statements
    def _docuvision_request(
        self,
        document: RequestDocument,
        response: DocuVisionSQSResponseMessage,
    ) -> None:
        """Send the document data to DocuVision set 2 service for processing and
        returning a prepared response message object.
        """
        if not response:
            return
        if document is None or not document.data or document.encodingType is None:
            response.state = hankai.orchestrator.ResponseState.ERROR
            response.error = hankai.orchestrator.ErrorTrace(
                "Document [data] or [encodingType] are empty. They are required.",
                None,
            )
        else:
            # Send the data to the processor.
            decoded_data = hankai.lib.Util.base_decode(
                encoded=document.data, base=document.encodingType.base
            )

            output_file = os.path.join(self.output_dir, str(threading.get_ident()))

            stdout, stderr, returncode = hankai.lib.Sys.run(
                cmd=[self.app, "--stdin", f"--output={output_file}"],
                stdin_input=decoded_data,
            )

            if stdout:
                self.logenv.logger.info(
                    "Processor job [id={}] standard out:\n{}",
                    response.id,
                    stdout,
                )

            if returncode != 0:
                response.state = hankai.orchestrator.ResponseState.ERROR
                response.error = hankai.orchestrator.ErrorTrace(
                    f"Processor return status code [{returncode}]; expecting [0]. "
                    f"Error: {str(stderr)}",
                    None,
                )
                self.logenv.logger.error(
                    "Processor job [id={}] return status code [{}]; expecting "
                    "[0]. Reason:\n{}",
                    response.id,
                    returncode,
                    stderr,
                )
            else:
                if stderr:
                    self.logenv.logger.warning(
                        "Processor job [id={}] standard error:\n{}",
                        response.id,
                        stderr,
                    )
                try:
                    response.state = hankai.orchestrator.ResponseState.COMPLETED
                    response.result = json.loads(
                        hankai.lib.Sys.read_file(file=output_file)
                    )
                except FileNotFoundError:
                    response.error = hankai.orchestrator.ErrorTrace(
                        message=f"Processor output file [{output_file}] was not found.",
                        tracebacks=hankai.lib.Util.formatted_traceback_exceptions(),
                    )
                    response.state = hankai.orchestrator.ResponseState.ERROR

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
        """Consumer function for DocuVision set 2 service AWS SQS requests queue.
        Processes message body delivery PDF data to the DocuVision set 1 service
        HTTP API. Results are sent to the DocuVision set 2 service AWS SQS responses
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
            results = response.result.get("RESULT", [])
            for result in results:
                result["OriginDocumentName"] = response.processedDocument.name

            pages = response.result.get("PAGES", [])
            for page in pages:
                page["filename"] = response.processedDocument.name

        response.metadata.processEndTime = hankai.lib.Util.date_now()
        response.statistics.processDurationSeconds = hankai.lib.Util.duration_seconds(
            start=response.metadata.processStartTime,
            end=response.metadata.processEndTime,
        )
