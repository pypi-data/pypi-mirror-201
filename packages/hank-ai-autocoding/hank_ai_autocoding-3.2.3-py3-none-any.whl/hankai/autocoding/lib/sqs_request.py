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
serialization/de-serialization."""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

import jsonpickle  # type: ignore[import]

import hankai.lib
import hankai.orchestrator

from .enum_other import SetService


@dataclass
class AutoCodingSQSRequestMessage(hankai.orchestrator.SQSRequestMessage):
    """AutoCodingSQSRequestMessage message."""

    request: Optional[Request] = None

    def redacted(self) -> AutoCodingSQSRequestMessage:
        """RedactString items that may contain PHI or would pollute the log."""
        req_copy = copy.deepcopy(self)
        if req_copy.request is not None and req_copy.request.job is not None:
            req_copy.request.job = {
                hankai.lib.RedactString.STRING.value: hankai.lib.RedactString.STRING.value
            }

        return req_copy

    @staticmethod
    def jsonpickle_handlers() -> List[hankai.orchestrator.JsonpickleHandler]:
        """List of SQSRequestMessage Jsonpickle handlers."""
        jsonpickle_handlers: List[hankai.orchestrator.JsonpickleHandler] = []
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.orchestrator.Service,
                handler=hankai.orchestrator.EnumPickling,
            )
        )

        return jsonpickle_handlers

    def validate(self, api_client: bool = False) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if not api_client and self.id is None:
            invalid.append("Message [AutoCodingSQSRequestMessage.id] is required.")
        if self.name is None:
            invalid.append("Message [AutoCodingSQSRequestMessage.name] is is required.")
        if self.request is None:
            invalid.append("Message [AutoCodingSQSRequestMessage.request] is required.")
        else:
            invalid.extend(self.request.validate())

        return invalid

    @staticmethod
    def unpicklable(message: Dict[str, Any]) -> AutoCodingSQSRequestMessage:
        """Set the SQSRequestMessage fields from the message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        req_msg = AutoCodingSQSRequestMessage()

        # pylint: disable=attribute-defined-outside-init
        req_msg.id = message.get("id")
        req_msg.name = message.get("name")
        req_msg.request = Request.unpicklable(request=message.get("request"))

        return req_msg

    @staticmethod
    def unpickle(
        message: Union[Dict[str, Any], str],
        redacted: bool = True,
        jsonpickle_decode_classes: Optional[Set[type]] = None,
    ) -> AutoCodingSQSRequestMessage:
        """Unpickle message to AutoCodingSQSResponseMessage."""
        if jsonpickle_decode_classes is None:
            jsonpickle_decode_classes = set()

        if AutoCodingSQSRequestMessage not in jsonpickle_decode_classes:
            jsonpickle_decode_classes.add(AutoCodingSQSRequestMessage)

        request_message: AutoCodingSQSRequestMessage

        msg_str: str = json.dumps(message) if not isinstance(message, str) else message
        msg_dict: Dict[str, Any] = (
            json.loads(message) if isinstance(message, str) else message
        )

        if msg_str and "py/object" in msg_str:
            request_message = jsonpickle.decode(
                msg_str, classes=jsonpickle_decode_classes
            )
            # Pylance thinks unnecessary, but it may not decode to the expected
            # class if the JSON body is not conformant.
            if not isinstance(request_message, AutoCodingSQSRequestMessage):
                raise AssertionError(
                    "Request message could not be decoded to "
                    f"[{AutoCodingSQSRequestMessage}] class."
                )
        else:
            request_message = AutoCodingSQSRequestMessage.unpicklable(message=msg_dict)

        del msg_str
        del msg_dict

        if redacted:
            return request_message.redacted()

        return request_message

    @staticmethod
    def factory(**kwargs: Any) -> AutoCodingSQSRequestMessage:
        """Convenience class to create a SQSRequestMessage."""
        name: str = kwargs["name"]
        request_file: hankai.lib.FileProperties = kwargs["request_file"]
        service: hankai.orchestrator.Service = kwargs["service"]
        data_key: Optional[str] = kwargs.get("data_key")
        req_id: Optional[int] = kwargs.get("req_id")
        api_client: bool = kwargs.get("api_client", False)

        request_file.encode_non_binary()
        job: Optional[Dict[str, Any]] = None

        if request_file.encoded:
            job = json.loads(request_file.encoded)
        request_msg = AutoCodingSQSRequestMessage(
            id=req_id,
            name=name,
            request=Request(
                service=service,
                job=job,
                dataKey=data_key,
            ),
        )

        invalids = request_msg.validate(api_client=api_client)
        if invalids:
            invalid_msg = "\n\t".join(invalids)
            raise ValueError(f"AutoCoding request message is invalid:\n\t{invalid_msg}")

        return request_msg


@dataclass
class Request(hankai.orchestrator.Request):
    """Request class."""

    # pylint: disable=invalid-name
    job: Optional[Dict[str, Any]] = None

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.service is None:
            invalid.append("Message [Request.service] is required.")
        if self.job is None:
            invalid.append("Message [Request.job] is required.")
        elif self.service:
            if not SetService.supported(service=self.service):
                invalid.append(
                    f"Message [Request.service={self.service}] is not supported."
                )

        return invalid

    @staticmethod
    def unpicklable(request: Optional[Dict[str, Any]]) -> Optional[Request]:
        """Set the Request message fields from the request dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if request is None:
            return None

        req = Request()
        req.service = hankai.orchestrator.Service.member_by(
            member=str(request.get("service"))
        )
        req.job = request.get("job")
        req.dataKey = request.get("dataKey")

        return req
