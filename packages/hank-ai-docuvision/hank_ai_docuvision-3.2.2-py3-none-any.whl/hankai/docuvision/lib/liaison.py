#!/usr/bin/env python3
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

"""DocuVision liaison to receive AWS SQS DocuVision request queue messages,
process the data via DocuVision service and respond with results to the AWS SQS
DocuVision responses queue.
"""
from dataclasses import dataclass
from typing import Optional, Type

import hankai.aws
import hankai.lib
import hankai.orchestrator

from .enum_other import ServiceFeature, SetService

# from .liaison_set_1_processor import LiaisonSet1Processor, LiaisonSet1ProcessorEnv
from .liaison_set_2_processor import LiaisonSet2Processor, LiaisonSet2ProcessorEnv
from .sqs_request import DocuVisionSQSRequestMessage
from .sqs_response import DocuVisionSQSResponseMessage


class DocuVisionLiaisonEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and DocuVisionLiaisonEnv attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_LIAISON_SERVICE = "service"


@dataclass
class DocuVisionLiaison(hankai.orchestrator.Liaison):
    """DocuVision liaison to receive AWS SQS message requests, process the data
    via DocuVision and respond with results to an AWS SQS responses queue.
    """

    service: hankai.orchestrator.Service = hankai.orchestrator.Service.DOCUVISION_1
    docuvision_liaison_env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.docuvision_liaison_env:
            self.logenv.env_supersede(
                clz=self,
                env_type=self.docuvision_liaison_env,
            )

        super().__post_init__()


@dataclass
class LiaisonFactory:
    """DocuVision liaison factory to collect the processor service."""

    service: hankai.orchestrator.Service
    unpicklable: bool
    backoff: hankai.lib.Backoff
    logenv: hankai.lib.LogEnv
    env: Optional[Type[hankai.lib.EnvEnum]] = None
    docuvision_liaison_env: Optional[Type[hankai.lib.EnvEnum]] = None

    def assemble(
        self,
    ) -> DocuVisionLiaison:
        """Based on the DocuVision service, collect the appropriate
        DocuVisionLiaison.
        """
        feature: str
        processor: hankai.orchestrator.LiaisonProcessor
        if self.service is hankai.orchestrator.Service.DOCUVISION_1:
            feature = SetService.features(  # type: ignore[assignment,union-attr]
                service_set=2,
                service=hankai.orchestrator.Service.DOCUVISION_1,
            ).get(ServiceFeature.APP)

            processor = LiaisonSet2Processor(
                service=hankai.orchestrator.Service.DOCUVISION_1,
                env=LiaisonSet2ProcessorEnv,
                app=feature,
                logenv=self.logenv,
            )
        elif self.service is hankai.orchestrator.Service.DOCUVISION_2:
            feature = SetService.features(  # type: ignore[assignment,union-attr]
                service_set=2,
                service=hankai.orchestrator.Service.DOCUVISION_2,
            ).get(ServiceFeature.APP)

            processor = LiaisonSet2Processor(
                service=hankai.orchestrator.Service.DOCUVISION_2,
                env=LiaisonSet2ProcessorEnv,
                app=feature,
                logenv=self.logenv,
            )
        elif self.service is hankai.orchestrator.Service.DOCUVISION_3:
            feature = SetService.features(  # type: ignore[assignment,union-attr]
                service_set=2,
                service=hankai.orchestrator.Service.DOCUVISION_3,
            ).get(ServiceFeature.APP)

            processor = LiaisonSet2Processor(
                service=hankai.orchestrator.Service.DOCUVISION_3,
                env=LiaisonSet2ProcessorEnv,
                app=feature,
                logenv=self.logenv,
            )
        else:
            raise ValueError(f"DocuVision service [{self.service}] is not supported.")

        requests_queue: hankai.aws.SimpleQueueService = hankai.aws.SimpleQueueService(
            servicer=hankai.aws.Servicer(
                session=hankai.aws.Session(
                    environment=hankai.aws.Environment(
                        env=hankai.orchestrator.EnvironmentSQSRequestsEnv,
                        logenv=self.logenv,
                    )
                ),
                service_name=hankai.aws.ServiceName.SIMPLE_QUEUE_SERVICE,
                env=hankai.orchestrator.ServicerSQSRequestsEnv,
                logenv=self.logenv,
            ),
            queue_name="env-must-supersede-requests-queue_name",
            env=hankai.orchestrator.SQSRequestsQueueEnv,
            logenv=self.logenv,
        )
        request_message: Type[DocuVisionSQSRequestMessage] = DocuVisionSQSRequestMessage
        responses_queue: hankai.aws.SimpleQueueService = hankai.aws.SimpleQueueService(
            servicer=hankai.aws.Servicer(
                session=hankai.aws.Session(
                    environment=hankai.aws.Environment(
                        env=hankai.orchestrator.EnvironmentSQSResponsesEnv,
                        logenv=self.logenv,
                    )
                ),
                service_name=hankai.aws.ServiceName.SIMPLE_QUEUE_SERVICE,
                env=hankai.orchestrator.ServicerSQSResponsesEnv,
                logenv=self.logenv,
            ),
            queue_name="env-must-supersede-responses-queue_name",
            env=hankai.orchestrator.SQSResponsesQueueEnv,
            logenv=self.logenv,
        )
        response_message: Type[
            DocuVisionSQSResponseMessage
        ] = DocuVisionSQSResponseMessage

        return DocuVisionLiaison(  # pylint: disable=unexpected-keyword-arg
            service=self.service,
            processor=processor,
            requests_queue=requests_queue,
            request_message=request_message,
            responses_queue=responses_queue,
            response_message=response_message,
            unpicklable=self.unpicklable,
            backoff=self.backoff,
            logenv=self.logenv,
            env=self.env,
            docuvision_liaison_env=self.docuvision_liaison_env,
        )
