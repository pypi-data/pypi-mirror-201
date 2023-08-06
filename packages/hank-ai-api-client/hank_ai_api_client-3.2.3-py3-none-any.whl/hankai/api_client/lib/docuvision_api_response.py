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
import pendulum
from pendulum.datetime import DateTime

import hankai.docuvision
import hankai.lib
import hankai.orchestrator


@dataclass
class DocuVisionAPIResponseMessage(  # pylint: disable=too-many-instance-attributes
    hankai.orchestrator.APIResponseMessage
):
    """Orchestrator response message."""

    response: Optional[DocuVisionAPIResponse] = None

    def redacted(self) -> DocuVisionAPIResponseMessage:
        """RedactString items that may contain PHI or would pollute the log."""
        res_copy = copy.deepcopy(self)
        if res_copy.response is not None and res_copy.response.result is not None:
            res_copy.response.result.RESULT = [hankai.lib.RedactString.STRING.value]
            res_copy.response.result.PAGES = [hankai.lib.RedactString.STRING.value]

        return res_copy

    @staticmethod
    def jsonpickle_handlers() -> List[hankai.orchestrator.JsonpickleHandler]:
        """List of DocuVisionSQSResponseMessage Jsonpickle handlers."""
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
        jsonpickle_handlers.append(
            hankai.orchestrator.JsonpickleHandler(
                cls=hankai.orchestrator.Model, handler=hankai.orchestrator.EnumPickling
            )
        )

        return jsonpickle_handlers

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.id is None:
            invalid.append("Message [DocuVisionAPIResponseMessage.id] is required.")
        if self.name is None:
            invalid.append("Message [DocuVisionAPIResponseMessage.name] is required.")
        if self.response is None:
            invalid.append(
                "Message [DocuVisionAPIResponseMessage.response] is required."
            )
        else:
            invalid.extend(self.response.validate())
        if self.state is None:
            invalid.append("Message [DocuVisionAPIResponseMessage.state] is required.")
        if self.metadata is None:
            invalid.append(
                "Message [DocuVisionSQSResponseMessage.metadata] is required."
            )

        return invalid

    @staticmethod
    def unpicklable(message: Dict[str, Any]) -> DocuVisionAPIResponseMessage:
        """Set the DocuVisionAPIResponseMessage fields from the message.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        res_msg = DocuVisionAPIResponseMessage()

        # pylint: disable=attribute-defined-outside-init, disable=invalid-name
        res_msg.id = message.get("id")
        res_msg.name = message.get("name")
        res_msg.description = message.get("description")
        res_msg.request = message.get("request")
        res_msg.response = DocuVisionAPIResponse.unpicklable(
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
    ) -> DocuVisionAPIResponseMessage:
        """Unpickle message to SQSResponseMessage."""
        if jsonpickle_decode_classes is None:
            jsonpickle_decode_classes = set()

        if DocuVisionAPIResponseMessage not in jsonpickle_decode_classes:
            jsonpickle_decode_classes.add(DocuVisionAPIResponseMessage)

        response_message: DocuVisionAPIResponseMessage

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
            if not isinstance(response_message, DocuVisionAPIResponseMessage):
                raise AssertionError(
                    "Request message could not be decoded to "
                    f"[{DocuVisionAPIResponseMessage}] class."
                )
        else:
            response_message = DocuVisionAPIResponseMessage.unpicklable(
                message=msg_dict
            )

        del msg_str
        del msg_dict

        if redacted:
            return response_message.redacted()

        return response_message


class DocuVisionAPIResponse:  # pylint: disable=too-many-instance-attributes, disable=invalid-name
    """DocuVisionAPIResponse class."""

    id: Optional[int] = None
    name: Optional[str] = None
    error: Optional[hankai.orchestrator.ErrorTrace] = None
    state: Optional[hankai.orchestrator.ResponseState] = None
    result: Optional[DocuVisionAPIResponseResult] = None
    status: Optional[str] = None
    service: Optional[hankai.orchestrator.Service] = None
    metadata: Optional[hankai.orchestrator.SQSResponseMetadata] = None
    statistics: Optional[hankai.orchestrator.SQSResponseStatistic] = None
    processedDocument: Optional[hankai.docuvision.RequestDocument] = None

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.id is None:
            invalid.append("Message [DocuVisionAPIResponse.id] is required.")
        if self.name is None:
            invalid.append("Message [DocuVisionAPIResponse.name] is required.")
        if self.state is None:
            invalid.append("Message [DocuVisionAPIResponse.state] is required.")
        if self.result is None:
            invalid.append("Message [DocuVisionAPIResponse.result] is required.")
        if self.service is None:
            invalid.append("Message [DocuVisionAPIResponse.service] is required.")
        if self.metadata is None:
            invalid.append("Message [DocuVisionAPIResponse.metadata] is required.")
        else:
            invalid.extend(self.metadata.validate())
        if self.statistics is None:
            invalid.append("Message [DocuVisionAPIResponse.statistics] is required.")
        else:
            invalid.extend(self.statistics.validate())
        if self.processedDocument is None:
            invalid.append(
                "Message [DocuVisionAPIResponse.processedDocument] is required."
            )
        elif self.service:
            invalid.extend(
                self.processedDocument.validate(
                    service=self.service, is_api_response=True
                )
            )

        return invalid

    @staticmethod
    def unpicklable(
        response: Optional[Dict[str, Any]]
    ) -> Optional[DocuVisionAPIResponse]:
        """Set the DocuVisionAPIResponse fields from message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if response is None:
            return None

        res = DocuVisionAPIResponse()

        res.id = response.get("id")
        res.name = response.get("name")
        res.error = hankai.orchestrator.ErrorTrace.unpicklable(
            error=response.get("error")
        )
        res.state = hankai.orchestrator.ResponseState.member_by(
            member=str(response.get("state"))
        )
        res.result = DocuVisionAPIResponseResult.unpicklable(
            result=response.get("result")
        )
        res.status = response.get("status")
        res.service = hankai.orchestrator.Service.member_by(
            member=str(response.get("service"))
        )
        res.metadata = hankai.orchestrator.SQSResponseMetadata.unpicklable(
            metadata=response.get("metadata")
        )
        res.statistics = hankai.orchestrator.SQSResponseStatistic.unpicklable(
            statistics=response.get("statistics")
        )
        res.processedDocument = hankai.docuvision.RequestDocument.unpicklable(
            document=response.get("processedDocument")
        )

        return res


@dataclass
class DocuVisionAPIResponseResult:
    """DocuVisionAPIResponseResult class."""

    # pylint: disable=invalid-name
    RESULT: Optional[List[Any]] = None
    METADATA: Optional[DocuVisionAPIResponseMetadata] = None
    PAGES: Optional[List[Any]] = None
    PIDS: Optional[List[Any]] = None

    @staticmethod
    def unpicklable(
        result: Optional[Dict[str, Any]]
    ) -> Optional[DocuVisionAPIResponseResult]:
        """Set the DocuVisionAPIResponseResult fields from message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if result is None:
            return None

        res_res = DocuVisionAPIResponseResult()

        res_res.RESULT = result.get("RESULT")
        res_res.METADATA = DocuVisionAPIResponseMetadata.unpicklable(
            metadata=result.get("METADATA")
        )
        res_res.PAGES = result.get("PAGES")
        res_res.PIDS = result.get("PIDS")

        return res_res


@dataclass
class DocuVisionAPIResponseMetadata:  # pylint: disable=too-many-instance-attributes
    """DocuVisionAPIResponseMetadata class."""

    # pylint: disable=invalid-name
    createdAt: Optional[DateTime] = None
    pagesProcessed: Optional[int] = None
    processingDuration_ms: Optional[int] = None
    apiVersion: Optional[str] = None
    outputSpec: Optional[str] = None

    def validate(self) -> List[str]:
        """Validate the fields."""
        invalid: List[str] = []
        if self.createdAt is None:
            invalid.append("Message [DocuVisionAPIResponse.createdAt] is required.")
        if self.pagesProcessed is None:
            invalid.append(
                "Message [DocuVisionAPIResponse.pagesProcessed] is required."
            )
        if self.processingDuration_ms is None:
            invalid.append(
                "Message [DocuVisionAPIResponse.processingDuration_ms] is required."
            )
        if self.apiVersion is None:
            invalid.append("Message [DocuVisionAPIResponse.apiVersion] is required.")
        if self.outputSpec is None:
            invalid.append("Message [DocuVisionAPIResponse.outputSpec] is required.")

        return invalid

    @staticmethod
    def unpicklable(
        metadata: Optional[Dict[str, Any]]
    ) -> Optional[DocuVisionAPIResponseMetadata]:
        """Set the DocuVisionAPIResponseMetadata fields from message dictionary.

        ! NOTE: Ideally this method should not exist. It's strongly encouraged
        to utilize the jsonpickle encode/decode for wire transmission. Using
        this method is hacky and doesn't allow for greater type hint utilization.
        """
        if metadata is None:
            return None

        meta = DocuVisionAPIResponseMetadata()

        create_time = metadata.get("createdAt")
        if create_time is not None:
            create_dt = pendulum.parse(create_time)
            if not isinstance(create_dt, DateTime):
                raise AssertionError(
                    f"Attribute [createdAt={create_time}] could not be "
                    "parsed to pendulum.DateTime."
                )
            meta.createdAt = create_dt
        meta.pagesProcessed = metadata.get("pagesProcessed")
        meta.processingDuration_ms = metadata.get("processingDuration_ms")
        meta.apiVersion = metadata.get("apiVersion")
        meta.outputSpec = metadata.get("outputSpec")

        return meta
