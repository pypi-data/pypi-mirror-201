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
"""Classes for AutoCoding SQS Request and Response message
serialization/de-serialization.
"""
from __future__ import annotations

import hankai.orchestrator

from .sqs_request import AutoCodingSQSRequestMessage
from .sqs_response import AutoCodingSQSResponseMessage


class AutoCodingSQSMessageCopy(hankai.orchestrator.SQSMessageCopy):
    """Convenience class to copy common fields from one message type to another."""

    @staticmethod
    def request_to_response(
        request: hankai.orchestrator.SQSRequestMessage,
        response: hankai.orchestrator.SQSResponseMessage,
    ) -> None:
        """Copy request message fields to response message fields."""
        if not isinstance(request, AutoCodingSQSRequestMessage):
            raise AssertionError(
                "Argument [request] must be AutoCodingSQSRequestMessage."
            )
        if not isinstance(response, AutoCodingSQSResponseMessage):
            raise AssertionError(
                "Argument [response] must be AutoCodingSQSResponseMessage"
            )
        response.id = request.id
        response.name = request.name
        if request.request:
            response.service = request.request.service
