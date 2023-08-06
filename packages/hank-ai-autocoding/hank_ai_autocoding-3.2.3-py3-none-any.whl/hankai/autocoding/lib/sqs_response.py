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
"""Classes for AutoCoding AWS SQS Request and Response message
serialization/de-serialization.
"""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

import jsonpickle  # type: ignore[import]

import hankai.lib
import hankai.orchestrator


@dataclass
class AutoCodingSQSResponseMessage(  # pylint: disable=too-many-instance-attributes
    hankai.orchestrator.SQSResponseMessage
):
    """AutoCodingSQSResponse message."""

    service: Optional[hankai.orchestrator.Service] = None

    @staticmethod
    def jsonpickle_handlers() -> List[hankai.orchestrator.JsonpickleHandler]:
        """List of AutoCodingSQSRequestMessage Jsonpickle handlers."""

        jsonpickle_handlers: List[hankai.orchestrator.JsonpickleHandler] = []
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.lib.MimeType, handler=hankai.orchestrator.EnumPickling
            )
        )
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.orchestrator.Service,
                handler=hankai.orchestrator.EnumPickling,
            )
        )

        return jsonpickle_handlers

    def redacted(self) -> AutoCodingSQSResponseMessage:
        """RedactString items that may contain PHI or would pollute the log."""
        res_copy = copy.deepcopy(self)
        if res_copy.result is not None:
            res_copy.result = hankai.lib.RedactString.STRING.value

        return res_copy

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.id is None:
            invalid.append("Message [AutoCodingSQSResponseMessage.id] is required.")
        if self.name is None:
            invalid.append("Message [AutoCodingSQSResponseMessage.name] is required.")
        if self.service is None:
            invalid.append(
                "Message [AutoCodingSQSResponseMessage.service] is is required."
            )
        if self.state is None:
            invalid.append("Message [AutoCodingSQSResponseMessage.state] is required.")
        if self.result is None:
            invalid.append("Message [AutoCodingSQSResponseMessage.result] is required.")
        if self.metadata is None:
            invalid.append(
                "Message [AutoCodingSQSResponseMessage.metadata] is required."
            )
        if self.statistics is None:
            invalid.append(
                "Message [AutoCodingSQSResponseMessage.statistics] is required."
            )
        elif self.service is not None and self.service not in [
            hankai.orchestrator.Service.AUTOCODING_1
        ]:
            invalid.append(
                "Message [AutoCodingSQSResponseMessage.service] is not " "supported."
            )

        return invalid

    @staticmethod
    def unpicklable(message: Dict[str, Any]) -> AutoCodingSQSResponseMessage:
        """Set the AutoCodingSQSResponseMessage fields from the message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        res_msg = AutoCodingSQSResponseMessage()

        # pylint: disable=attribute-defined-outside-init, disable=invalid-name
        res_msg.id = message.get("id")
        res_msg.name = message.get("name")
        res_msg.service = hankai.orchestrator.Service.member_by(
            member=str(message.get("service"))
        )
        res_msg.state = hankai.orchestrator.ResponseState.member_by(
            str(message.get("state"))
        )
        res_msg.status = message.get("status")
        res_msg.error = hankai.orchestrator.ErrorTrace.unpicklable(
            error=message.get("error")
        )
        res_msg.result = message.get("result")
        res_msg.metadata = hankai.orchestrator.SQSResponseMetadata.unpicklable(
            metadata=message.get("metadata", {})
        )
        res_msg.statistics = hankai.orchestrator.SQSResponseStatistic.unpicklable(
            statistics=message.get("statistics", {})
        )

        return res_msg

    @staticmethod
    def unpickle(
        message: Union[Dict[str, Any], str],
        redacted: bool = True,
        jsonpickle_decode_classes: Optional[Set[type]] = None,
    ) -> AutoCodingSQSResponseMessage:
        """Unpickle message to AutoCodingSQSResponseMessage."""
        if jsonpickle_decode_classes is None:
            jsonpickle_decode_classes = set()

        if AutoCodingSQSResponseMessage not in jsonpickle_decode_classes:
            jsonpickle_decode_classes.add(AutoCodingSQSResponseMessage)

        response_message: AutoCodingSQSResponseMessage

        msg_str: str = json.dumps(message) if not isinstance(message, str) else message
        msg_dict: Dict[str, Any] = (
            json.loads(message) if isinstance(message, str) else message
        )

        if msg_str and "py/object" in msg_str:
            response_message = jsonpickle.decode(
                msg_str, classes=jsonpickle_decode_classes
            )
            # Pylance thinks unnecessary, but it may not decode to the expected
            # class if the JSON body is not conformant.
            if not isinstance(response_message, AutoCodingSQSResponseMessage):
                raise AssertionError(
                    "Request message could not be decoded to "
                    f"[{AutoCodingSQSResponseMessage}] class."
                )
        else:
            response_message = AutoCodingSQSResponseMessage.unpicklable(
                message=msg_dict
            )

        del msg_str
        del msg_dict

        if redacted:
            return response_message.redacted()

        return response_message
