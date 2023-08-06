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
"""Classes for Orchestrator DocuVison Response message
serialization/de-serialization.
"""
from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Union

import jsonpickle  # type: ignore[import]
from pendulum.datetime import DateTime

import hankai.lib
import hankai.orchestrator


@dataclass
class AutoCodingAPIResponseMessage(  # pylint: disable=too-many-instance-attributes
    hankai.orchestrator.APIResponseMessage
):
    """Orchestrator response message."""

    response: Optional[AutoCodingAPIResponse] = None

    def redacted(self) -> AutoCodingAPIResponseMessage:
        """RedactString items that may contain PHI or would pollute the log."""
        res_copy = copy.deepcopy(self)
        if res_copy.response is not None and res_copy.response.result is not None:
            res_copy.response.result = hankai.lib.RedactString.STRING.value

        return res_copy

    @staticmethod
    def jsonpickle_handlers() -> List[hankai.orchestrator.JsonpickleHandler]:
        """List of AutoCodingSQSResponseMessage Jsonpickle handlers."""
        jsonpickle_handlers: List[hankai.orchestrator.JsonpickleHandler] = []
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.orchestrator.ResponseState,
                handler=hankai.orchestrator.EnumPickling,
            )
        )
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.orchestrator.ErrorTrace,
                handler=hankai.orchestrator.ErrorTracePickling,
            )
        )
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.lib.MimeType, handler=hankai.orchestrator.EnumPickling
            )
        )
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=DateTime, handler=hankai.orchestrator.DateTimePickling
            )
        )
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.orchestrator.Service,
                handler=hankai.orchestrator.EnumPickling,
            )
        )

        return jsonpickle_handlers

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.id is None:
            invalid.append("Message [AutoCodingAPIResponseMessage.id] is required.")
        if self.name is None:
            invalid.append("Message [AutoCodingAPIResponseMessage.name] is required.")
        if self.response is None:
            invalid.append(
                "Message [AutoCodingAPIResponseMessage.response] is required."
            )
        else:
            invalid.extend(self.response.validate())
        if self.state is None:
            invalid.append("Message [AutoCodingAPIResponseMessage.state] is required.")
        if self.metadata is None:
            invalid.append(
                "Message [AutoCodingSQSResponseMessage.metadata] is required."
            )

        return invalid

    @staticmethod
    def unpicklable(message: Dict[str, Any]) -> AutoCodingAPIResponseMessage:
        """Set the AutoCodingAPIResponseMessage fields from the message.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        res_msg = AutoCodingAPIResponseMessage()

        # pylint: disable=attribute-defined-outside-init, disable=invalid-name
        res_msg.id = message.get("id")
        res_msg.name = message.get("name")
        res_msg.description = message.get("description")
        res_msg.request = message.get("request")
        res_msg.response = AutoCodingAPIResponse.unpicklable(
            response=message.get("response")
        )
        res_msg.state = hankai.orchestrator.ResponseState.member_by(
            member=str(message.get("state"))
        )
        res_msg.status = message.get("status")
        res_msg.metadata = hankai.orchestrator.APIResponseMetadata.unpicklable(
            metadata=message.get("metadata")
        )
        res_msg.error = hankai.orchestrator.ErrorTrace.unpicklable(
            error=message.get("error")
        )

        return res_msg

    @staticmethod
    def unpickle(
        message: Union[Dict[str, Any], str],
        redacted: bool = False,
        jsonpickle_decode_classes: Optional[Set[type]] = None,
    ) -> AutoCodingAPIResponseMessage:
        """Unpickle message to SQSResponseMessage."""
        if jsonpickle_decode_classes is None:
            jsonpickle_decode_classes = set()

        if AutoCodingAPIResponseMessage not in jsonpickle_decode_classes:
            jsonpickle_decode_classes.add(AutoCodingAPIResponseMessage)

        response_message: AutoCodingAPIResponseMessage

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
            if not isinstance(response_message, AutoCodingAPIResponseMessage):
                raise AssertionError(
                    "Request message could not be decoded to "
                    f"[{AutoCodingAPIResponseMessage}] class."
                )
        else:
            response_message = AutoCodingAPIResponseMessage.unpicklable(
                message=msg_dict
            )

        del msg_str
        del msg_dict

        if redacted:
            return response_message.redacted()

        return response_message


class AutoCodingAPIResponse:  # pylint: disable=too-many-instance-attributes, disable=invalid-name
    """AutoCodingAPIResponse class."""

    result: Optional[Any] = None

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.result is None:
            invalid.append("Message [AutoCodingAPIResponse.result] is required.")

        return invalid

    @staticmethod
    def unpicklable(
        response: Optional[Dict[str, Any]]
    ) -> Optional[AutoCodingAPIResponse]:
        """Set the AutoCodingAPIResponse fields from message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if response is None:
            return None

        res = AutoCodingAPIResponse()

        res.result = response.get("result")

        return res
