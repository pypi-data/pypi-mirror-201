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

"""AutoCoding liaison to receive AWS SQS AutoCoding request queue messages,
process the data via AutoCoding service and respond with results to the AWS SQS
AutoCoding responses queue.
"""
from dataclasses import dataclass
from typing import Optional, Type

import hankai.aws
import hankai.lib
import hankai.orchestrator

from .liaison_set_1_processor import LiaisonSet1Processor, LiaisonSet1ProcessorEnv
from .sqs_request import AutoCodingSQSRequestMessage
from .sqs_response import AutoCodingSQSResponseMessage


class AutoCodingLiaisonEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and AutoCodingLiaisonEnv attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_LIAISON_SERVICE = "service"


@dataclass
class AutoCodingLiaison(hankai.orchestrator.Liaison):
    """AutoCoding liaison to receive AWS SQS message requests, process the data
    via AutoCoding and respond with results to an AWS SQS responses queue.
    """

    service: hankai.orchestrator.Service = hankai.orchestrator.Service.AUTOCODING_1
    autocoding_liaison_env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.autocoding_liaison_env:
            self.logenv.env_supersede(
                clz=self,
                env_type=self.autocoding_liaison_env,
            )

        super().__post_init__()


@dataclass
class LiaisonFactory:
    """AutoCoding liaison factory to collect the processor service."""

    service: hankai.orchestrator.Service
    unpicklable: bool
    backoff: hankai.lib.Backoff
    logenv: hankai.lib.LogEnv
    env: Optional[Type[hankai.lib.EnvEnum]] = None
    autocoding_liaison_env: Optional[Type[hankai.lib.EnvEnum]] = None

    def assemble(
        self,
    ) -> AutoCodingLiaison:
        """Based on the AutoCoding service, collect the appropriate
        AutoCodingLiaison.
        """
        processor: hankai.orchestrator.LiaisonProcessor
        if self.service is hankai.orchestrator.Service.AUTOCODING_1:
            processor = LiaisonSet1Processor(
                service=hankai.orchestrator.Service.AUTOCODING_1,
                env=LiaisonSet1ProcessorEnv,
                logenv=self.logenv,
            )
        else:
            raise ValueError(f"AutoCoding service [{self.service}] is not supported.")

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
        request_message: Type[AutoCodingSQSRequestMessage] = AutoCodingSQSRequestMessage
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
            AutoCodingSQSResponseMessage
        ] = AutoCodingSQSResponseMessage

        return AutoCodingLiaison(  # pylint: disable=unexpected-keyword-arg
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
            autocoding_liaison_env=self.autocoding_liaison_env,
        )
