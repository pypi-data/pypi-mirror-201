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
"""Classes for AutoCodingProcessor request message processing."""
import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type

import hankai.aws
import hankai.lib
import hankai.orchestrator

from .sqs import AutoCodingSQSMessageCopy
from .sqs_request import AutoCodingSQSRequestMessage
from .sqs_response import AutoCodingSQSResponseMessage

# Append path to assure the 'production' autocoding processor
# models are referenced before the PASS BERTModel and Model. The PASS class
# files are to enable the api-client to instantiate on client systems that
# would not have the autocoding-core libraries installed.
autocoding_core_paths: List[str] = ["/app/autocoding-core", "/app/autocoding-core/src"]
core_exists: bool = False
for path in autocoding_core_paths:
    if os.path.exists(path):
        core_exists = True  # pylint: disable=invalid-name
        sys.path.append(path)

# pylint: disable=import-error, disable=wrong-import-order, disable=wrong-import-position, disable=no-name-in-module
if core_exists:
    from src.BERTModel import BERTModel  # type: ignore[import] # pants: no-infer-dep
    from src.Model import Model  # type: ignore[import] # pants: no-infer-dep
else:
    from .no_core_models import BERTModel, Model


class LiaisonSet1ProcessorEnv(hankai.lib.EnvEnum):
    """LiaisonSet1Processor EnvEnum for hankai.AutoCoding1Processor."""

    HANK_AUTOCODING_LIAISON_PROCESSOR_API_VERSION = "api_version"


@dataclass
class LiaisonSet1Processor(hankai.orchestrator.LiaisonProcessor):
    """LiaisonProcessor class which awaits the AutoCoding service being
    ready/available and sends a response for the processed request. The
    read_flag_path is set by the AutoCoding application. To set other
    ENV for SimpleQueueService see
    hankai.aws.resource.sqs.SimpleQueueServiceEnv.
    """

    service: hankai.orchestrator.Service
    logenv: hankai.lib.LogEnv
    api_version: str = "1.0.0"
    processor: Model = BERTModel()
    processor_predictor_warm_up_job: str = "/tmp/warm-up-job.json"
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

    def is_ready(self) -> bool:
        """Wait for AutoCoding predict to load up."""
        self.logenv.logger.info(
            "Waiting for AutoCoding service [{}] processor model [{}] predictor "
            "to become ready. Warming up model predictor with sample job [{}]",
            self.service,
            type(self.processor),
            self.processor_predictor_warm_up_job,
        )
        job = hankai.lib.Sys.read_file(self.processor_predictor_warm_up_job)
        self.processor.predict(job)
        self.logenv.logger.info(
            "AutoCoding service [{}] processor is ready to receive requests.",
            self.service,
        )
        return True

    # pylint: disable=too-many-branches disable=too-many-statements
    def _autocoding_request(
        self,
        job: Dict[str, Any],
        response: AutoCodingSQSResponseMessage,
    ) -> None:
        """Send the document data to AutoCoding for processing and returning a
        prepared response message object.
        """
        if not response:
            return

        response.state = hankai.orchestrator.ResponseState.ERROR

        if job is None:
            response.error = hankai.orchestrator.ErrorTrace(  # type: ignore[unreachable]
                "Argument [job] is empty. It is required.", None
            )
            return

        try:
            response.result = self.processor.predict(json.dumps(job))
            response.state = hankai.orchestrator.ResponseState.COMPLETED
        except Exception:  # pylint: disable=broad-except
            self.logenv.logger.exception("Unexpected exception from the processor.")
            response.error = hankai.orchestrator.ErrorTrace(
                "Unexpected exception from the processor.",
                hankai.lib.Util.formatted_traceback_exceptions(),
            )

    def init_response(
        self,
        request: hankai.orchestrator.SQSRequestMessage,
    ) -> AutoCodingSQSResponseMessage:
        """Initialize the response message based on the request message."""
        if not isinstance(request, AutoCodingSQSRequestMessage):
            raise AssertionError(
                "Argument [request] must be AutoCodingSQSRequestMessage."
            )
        response = AutoCodingSQSResponseMessage()
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
        """Consumer function for AutoCoding set 1 service AWS SQS requests queue.
        Processes message body delivery PDF data to the AutoCoding HTTP API.
        Results are sent to the AutoCoding AWS SQS responses queue.

        ! NOTE: This is primarily a Callable reference method for
        LiaisonWorkers. Other use cases have not been tested.

        https://docs.aws.amazon.com/SimpleQueueService/latest/SQSDeveloperGuide/using-messagegroupid-property.html
        """
        if not isinstance(request, AutoCodingSQSRequestMessage):
            raise AssertionError(
                "Argument [request] must be AutoCodingSQSRequestMessage"
            )
        if not isinstance(response, AutoCodingSQSResponseMessage):
            raise AssertionError(
                "Argument [response] must be AutoCodingSQSResponseMessage"
            )
        AutoCodingSQSMessageCopy.request_to_response(request=request, response=response)

        if (  # pylint: disable=too-many-boolean-expressions
            not request.request
            or not request.request.job
            or not response
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
            self._autocoding_request(
                job=request.request.job,
                response=response,
            )

        response.metadata.processEndTime = hankai.lib.Util.date_now()
        response.statistics.processDurationSeconds = hankai.lib.Util.duration_seconds(
            start=response.metadata.processStartTime,
            end=response.metadata.processEndTime,
        )
