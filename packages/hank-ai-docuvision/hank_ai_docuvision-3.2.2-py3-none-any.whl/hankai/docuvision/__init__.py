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
"""Hank AI DocuVision lib initialization."""
from hankai.docuvision.lib.enum_other import *
from hankai.docuvision.lib.liaison import *
from hankai.docuvision.lib.liaison_set_1_processor import *
from hankai.docuvision.lib.liaison_set_2_processor import *
from hankai.docuvision.lib.sqs import *
from hankai.docuvision.lib.sqs_request import *
from hankai.docuvision.lib.sqs_response import *

__all__ = [
    "DocuVisionLiaison",
    "DocuVisionLiaisonEnv",
    "DocuVisionSQSMessageCopy",
    "DocuVisionSQSResponseMessage",
    "DocuVisionSQSRequestMessage",
    "LiaisonFactory",
    "LiaisonSet1Processor",
    "LiaisonSet1ProcessorEnv",
    "LiaisonSet1Processor",
    "LiaisonSet1ProcessorEnv",
    "ResponseDocument",
    "Request",
    "RequestDocument",
    "ServiceFeature",
    "SetService",
]

__version__ = "3.2.2"
