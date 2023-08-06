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
"""Orchestrator scaling manager for auto scaling in/out various AWS compute
resources.
"""

import hankai.autocoding
import hankai.aws
import hankai.lib
import hankai.orchestrator


# ------------------------------------------------------------------------------
def main():
    """Start AutoCoding scaling manager. All ScalingManagerEC2ASGAndECSBySQS
    ENV supersede classes are defined in that class. Use these classes for ENV
    supersede:
    hankai.aws.EnvironmentEnv
    ServicerECSEnv
    ServicerSQSEnv
    hankai.aws.SimpleQueueServiceEnv
    hankai.aws.SQSScaleEnv
    hankai.aws.ElasticContainerServiceEnv
    hankai.aws.ScaleECSEnv
    hankai.lib.LogEnvEnv
    hankai.lib.BackoffEnv
    hankai.lib.ErrorExitEnv
    """
    logenv = hankai.lib.LogEnv(env=hankai.lib.LogEnvEnv)
    backoff = hankai.lib.Backoff(env=hankai.lib.BackoffEnv)
    error_exit = hankai.lib.ErrorExit(
        env=hankai.lib.ErrorExitEnv,
        logenv=logenv,
    )

    logenv.logger.info(
        "Module Versions: hankai.lib [{}], hankai.aws [{}], hankai.orchestrator "
        "[{}], hankai.autocoding [{}]",
        hankai.lib.__version__,
        hankai.aws.__version__,
        hankai.orchestrator.__version__,
        hankai.autocoding.__version__,
    )

    while True:
        try:
            hankai.orchestrator.ScalingManagerECSBySQS(
                logenv=logenv,
                backoff=backoff,
            ).start()
        except Exception as exc:  # pylint: disable=broad-except
            error_exit.exception_handler(exception=exc)
