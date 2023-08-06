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
"""Orchestrator liaison to receive AWS SQS Orchestrator request queue messages,
process the data via Orchestrator service and respond with results to the AWS SQS
Orchestrator responses queue.
"""
import sys
from typing import Optional

import hankai.aws
import hankai.docuvision
import hankai.lib
import hankai.orchestrator


# ------------------------------------------------------------------------------
def main():
    """Start DocuVision liaison by service name."""
    service_arg: str = sys.argv[1]
    supported = hankai.docuvision.SetService.supported(service=service_arg)
    if not supported:
        raise ValueError(
            f"Service [{service_arg}] is not supported. Service must be one of "
            f"[{'|'.join(hankai.docuvision.SetService.services_str())}]."
        )
    service: Optional[
        hankai.orchestrator.Service
    ] = hankai.orchestrator.Service.member_by(member=service_arg)
    if service is None:
        raise AssertionError(f"Service [{service_arg}] could not be resolved.")

    logenv = hankai.lib.LogEnv(env=hankai.lib.LogEnvEnv)
    backoff = hankai.lib.Backoff(env=hankai.lib.BackoffEnv)
    error_exit = hankai.lib.ErrorExit(
        env=hankai.lib.ErrorExitEnv,
        logenv=logenv,
    )

    logenv.logger.info(
        "Module Versions: hankai.lib [{}], hankai.aws [{}], hankai.orchestrator "
        "[{}], hankai.docuvision [{}]",
        hankai.lib.__version__,
        hankai.aws.__version__,
        hankai.orchestrator.__version__,
        hankai.docuvision.__version__,
    )

    while True:
        try:
            hankai.docuvision.LiaisonFactory(
                service=service,
                unpicklable=False,
                backoff=backoff,
                logenv=logenv,
                env=hankai.orchestrator.LiaisonEnv,
                docuvision_liaison_env=hankai.docuvision.DocuVisionLiaisonEnv,
            ).assemble().start()
        except Exception as exc:  # pylint: disable=broad-except
            error_exit.exception_handler(exception=exc)
