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

"""HANK API Mock Message utility."""

import argparse
import json
import os
import random
import sys
import time
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple, Union

import jsonpickle  # type: ignore[import]

import hankai.api_client
import hankai.autocoding
import hankai.aws
import hankai.docuvision
import hankai.lib
import hankai.orchestrator


@dataclass
class MockMessage:  # pylint: disable=too-many-instance-attributes
    """MockMessage class. Create mock AWS SQS request
    messages for testing."""

    encoding: hankai.lib.Encoding = hankai.api_client.MockDefault.encoding
    mime_type: hankai.lib.MimeType = hankai.api_client.MockDefault.mime_type
    confidence_interval: float = hankai.api_client.MockDefault.confidence_interval
    perform_ocr: bool = hankai.api_client.MockDefault.perform_ocr
    data_key: Optional[str] = None
    response_state: hankai.orchestrator.ResponseState = (
        hankai.api_client.MockDefault.response_state
    )
    redact: bool = hankai.api_client.MockDefault.redact
    picklable: bool = hankai.api_client.MockDefault.picklable
    version: bool = False

    # pylint: disable=too-many-statements, disable=too-many-branches
    def __post_init__(self) -> None:
        self.logenv = hankai.lib.LogEnv()
        self.args: argparse.Namespace = hankai.api_client.MockArgparse.namespace()

        if self.args.version:
            print(hankai.api_client.__version__)
            sys.exit(0)

        service: Optional[
            hankai.orchestrator.Service
        ] = hankai.orchestrator.Service.member_by(self.args.service)
        if service is None:
            raise ValueError(
                f"Option [--service={self.args.service}] is not supported."
            )
        self.service = service

        self.service_family = hankai.orchestrator.ServiceFamilies.family(
            service=self.service
        )

        if self.args.model:
            model = hankai.orchestrator.Model.member_by(self.args.model)
            if model is None:
                raise ValueError(
                    f"Option [--model] must be one of {hankai.orchestrator.Model.members()}."
                )
            self.model = model

        if self.args.encoding:
            encoding = hankai.lib.Encoding.unpicklable(encoding_type=self.args.encoding)
            if encoding is None:
                raise ValueError(
                    "Option [--encoding] must be one of encoding base "
                    f"{hankai.lib.EncodeBinaryBase.members()} and one of "
                    f"decoding codec {hankai.lib.EncodeStringCodec.members()}."
                )
            self.encoding = encoding

        if self.args.mime_type:
            mime_type = hankai.lib.MimeType.member_by(member=self.args.mime_type)
            if mime_type is None:
                raise ValueError(
                    "Option [--mime-type] is not a supported mime type. It "
                    f"must be one of {hankai.lib.MimeType.members()}."
                )
            self.mime_type = mime_type

        if self.args.confidence_interval is not None:
            self.confidence_interval = self.args.confidence_interval

        if (
            self.confidence_interval < hankai.orchestrator.ConfidenceInterval.MIN.value
            or self.confidence_interval
            > hankai.orchestrator.ConfidenceInterval.MAX.value
        ):
            raise ValueError(
                "Option [confidence_interval] minium  "
                f"[{hankai.orchestrator.ConfidenceInterval.MIN}], maximum "
                f"[{hankai.orchestrator.ConfidenceInterval.MAX}]."
            )

        if self.args.no_perform_ocr is not None:
            self.perform_ocr = self.args.no_perform_ocr

        if self.args.data_key:
            self.data_key = self.args.data_key

        if self.args.response_state:
            response_state = hankai.orchestrator.ResponseState.member_by(
                self.args.response_state
            )
            if response_state is None:
                raise ValueError(
                    "Option [--response-state] must be one of "
                    f"{hankai.orchestrator.ResponseState.members()}."
                )
            self.response_state = response_state

        if self.args.verbosity:
            self.logenv.set_verbosity(level=self.args.verbosity)

        if self.args.log_level:
            log_level = hankai.lib.LoguruLevel.member_by(member=self.args.log_level)
            if log_level is None:
                raise ValueError(
                    "Option [--log-level] must be one of "
                    f"{hankai.lib.LoguruLevel.members()}"
                )

            self.logenv.set_log_level(level=log_level)

        if self.args.no_redact is not None:
            self.redact = self.args.no_redact

        if self.args.picklable:
            self.picklable = True

        if (  # pylint: disable=too-many-boolean-expressions
            self.args.send_request
            or self.args.send_response
            or self.args.receive_request
            or self.args.delete_request
            or self.args.full_life_cycle
            or self.args.requests_queue_attributes
        ):
            environment = hankai.aws.Environment(
                env=hankai.aws.EnvironmentEnv,
                logenv=self.logenv,
            )
            session = hankai.aws.Session(environment=environment)
            servicer = hankai.aws.Servicer(
                session=session,
                service_name=hankai.aws.ServiceName.SIMPLE_QUEUE_SERVICE,
                env=hankai.aws.ServicerEnv,
                logenv=self.logenv,
            )
            if (
                self.args.receive_request
                or self.args.send_request
                or self.args.delete_request
                or self.args.full_life_cycle
                or self.args.requests_queue_attributes
            ):
                self.sqs_requests = hankai.aws.SimpleQueueService(
                    servicer=servicer,
                    queue_name=self.args.requests_queue,
                    max_messages=1,
                    s3_bucket=self.args.requests_s3_bucket,
                    s3_always=self.args.no_s3_always,
                    logenv=self.logenv,
                )
            if self.args.send_response or self.args.full_life_cycle:
                self.sqs_responses = hankai.aws.SimpleQueueService(
                    servicer=servicer,
                    queue_name=self.args.responses_queue,
                    max_messages=1,
                    s3_bucket=self.args.responses_s3_bucket,
                    s3_always=self.args.no_s3_always,
                    logenv=self.logenv,
                )

    # pylint: disable=too-many-branches
    def generate_request_message(
        self,
    ) -> hankai.orchestrator.SQSRequestMessage:
        """Create mock request."""
        file_properties = hankai.lib.FileProperties(
            path=self.args.document,
            source_path=os.path.dirname(self.args.document),
            encoding=self.encoding,
        )

        req_id: Optional[int] = None  # Client requests should have id=null
        if not self.args.generate_client_request and not self.args.full_life_cycle:
            req_id = random.randint(1, 999999999)

        req_name = file_properties.name
        if self.args.name:
            req_name = self.args.name

        request: hankai.orchestrator.SQSRequestMessage

        if self.service_family is hankai.orchestrator.ServiceFamily.AUTOCODING:
            request = hankai.autocoding.AutoCodingSQSRequestMessage.factory(
                name=req_name,
                service=self.service,
                request_file=file_properties,
                req_id=req_id,
                data_key=self.data_key,
                api_client=True,
            )
        elif self.service_family is hankai.orchestrator.ServiceFamily.DOCUVISION:
            request = hankai.docuvision.DocuVisionSQSRequestMessage.factory(
                req_id=req_id,
                name=req_name,
                request_file=file_properties,
                service=self.service,
                model=self.model,
                confidence_interval=self.confidence_interval,
                perform_ocr=self.perform_ocr,
                data_key=self.data_key,
                api_client=True,
            )

        if file_properties.mime_type is None and self.mime_type:
            file_properties.mime_type = self.mime_type

        if file_properties.mime_type is None:
            raise ValueError(
                "Unable to determine document mime type based on the document "
                "extension and [--mime-type] was not provided."
            )

        return request

    def generate_response_message(
        self,
        message: Optional[hankai.orchestrator.SQSRequestMessage] = None,
    ) -> hankai.orchestrator.SQSResponseMessage:
        """Generate HANK AI API  response messages."""
        if message is None:
            message = self.generate_request_message()

        response: hankai.orchestrator.SQSResponseMessage

        if self.service_family is hankai.orchestrator.ServiceFamily.AUTOCODING:
            response = hankai.autocoding.AutoCodingSQSResponseMessage()
            hankai.autocoding.AutoCodingSQSMessageCopy.request_to_response(
                message, response
            )
        elif self.service_family is hankai.orchestrator.ServiceFamily.DOCUVISION:
            response = hankai.docuvision.DocuVisionSQSResponseMessage()
            hankai.docuvision.DocuVisionSQSMessageCopy.request_to_response(
                message, response
            )

        response.state = self.response_state
        if response.state == hankai.orchestrator.ResponseState.ERROR:
            try:
                raise ValueError("Mock value error for traceback.")
            except ValueError:
                response.error = hankai.orchestrator.ErrorTrace(
                    "Mock error with traceback.",
                    hankai.lib.Util.formatted_traceback_exceptions(),
                )

        response.result = {"mock-response": "mock"}
        response.metadata = hankai.orchestrator.SQSResponseMetadata()
        response.statistics = hankai.orchestrator.SQSResponseStatistic()

        response.metadata.apiVersion = "1.0.1"
        response.metadata.processStartTime = hankai.lib.Util.date_now()
        response.metadata.processEndTime = hankai.lib.Util.date_now().add(minutes=1)
        response.statistics.processDurationSeconds = hankai.lib.Util.duration_seconds(
            start=response.metadata.processStartTime,
            end=response.metadata.processEndTime,
        )

        return response

    def format_message(
        self,
        message: Union[
            hankai.orchestrator.SQSRequestMessage,
            hankai.orchestrator.SQSResponseMessage,
        ],
    ) -> str:
        """Print the request message."""
        log_message = message.pickle(
            redacted=self.redact,
            unpicklable=self.picklable,
            indent=2,
            separators=hankai.lib.JsonPickleSeparator.DEFAULT,
            jsonpickle_handlers=message.jsonpickle_handlers(),
        )

        return log_message

    def send_mock_request(self) -> Any:
        """Send the mock HANK AI API  request message and return the AWS SQS
        response.
        """
        return self.send_request(message=self.generate_request_message())

    def send_request(self, message: hankai.orchestrator.SQSRequestMessage) -> Any:
        """Send the mock HANK AI API  request message and return the AWS SQS
        response.
        """
        response = self.sqs_requests.send_message(
            message=message.pickle(unpicklable=self.args.picklable),
        )

        self.logenv.logger.debug(
            "Sent HANK AI API  request message:\n{}\n::::\n{}",
            self.format_message(message=message),
            jsonpickle.encode(response, unpicklable=self.picklable, indent=2)
            if self.logenv.verbosity > 0
            else "(response redacted; verbosity < 1)",
        )

        return response

    def send_mock_response(self) -> Any:
        """Send the mock HANK AI API  response message and return the AWS SQS
        response.
        """
        return self.send_response(message=self.generate_response_message())

    def send_response(self, message: hankai.orchestrator.SQSResponseMessage) -> Any:
        """Send the HANK AI API  response message and return the AWS SQS
        response.
        """
        response = self.sqs_responses.send_message(
            message=message.pickle(unpicklable=self.picklable),
        )

        self.logenv.logger.debug(
            "Sent HANK AI API  response message:\n{}\n::::\n{}",
            self.format_message(message=message),
            jsonpickle.encode(response, unpicklable=self.picklable, indent=2)
            if self.logenv.verbosity > 0
            else "(response redacted; verbosity < 1)",
        )

        return response

    def receive_request(
        self,
    ) -> Optional[Tuple[str, hankai.orchestrator.SQSRequestMessage]]:
        """Receive the mock HANK AI API request message and return the AWS SQS
        receipt_handle and the HANK AI API SQSRequestMessage.
        """
        messages: List[
            hankai.aws.SQSMessage
        ] = self.sqs_requests.client_receive_message()
        if not messages:
            return None

        request_msg: Optional[hankai.orchestrator.SQSRequestMessage] = None
        # Receive was limited to maximum 1 message.
        receipt: str = ""

        for message in messages:
            if message.receipt_handle:
                self.logenv.logger.debug(
                    "Received HANK AI API request message [message_id={}], "
                    "[receipt_handle={}], [attributes={}], "
                    "[message_attributes={}], [md5_of_body={}], "
                    "[md5_of_message_attributes={}], [queue_url={}]:\n{}",
                    message.message_id,
                    message.receipt_handle,
                    message.attributes,
                    message.message_attributes,
                    message.md5_of_body,
                    message.md5_of_message_attributes,
                    message.queue_url,
                    message.body
                    if self.logenv.verbosity > 0
                    else "(body redacted; verbosity < 1)",
                )
                receipt = message.receipt_handle

                if message.body:
                    if (
                        self.service_family
                        is hankai.orchestrator.ServiceFamily.AUTOCODING
                    ):
                        request_msg = (
                            hankai.autocoding.AutoCodingSQSRequestMessage.unpicklable(
                                message=json.loads(message.body)
                            )
                        )
                    elif (
                        self.service_family
                        is hankai.orchestrator.ServiceFamily.DOCUVISION
                    ):
                        request_msg = (
                            hankai.docuvision.DocuVisionSQSRequestMessage.unpicklable(
                                message=json.loads(message.body)
                            )
                        )
                        break

        if not receipt or not request_msg:
            return None

        return (receipt, request_msg)

    def delete_request(self, receipt: str) -> None:
        """Delete the mock HANK AI API  request message."""
        self.sqs_requests.delete_message(receipt_handle=receipt)
        self.logenv.logger.debug(
            "Deleted HANK AI API  request message [receipt_handle={}] "
            "from request queue [{}].",
            receipt,
            self.sqs_requests.queue_name,
        )


def main():
    """Create HANK AI API  mock request messages."""
    mock = MockMessage()
    if mock.args.requests_queue_attributes:
        print(json.dumps(mock.sqs_requests.attributes(), indent=2))
    elif mock.args.generate_request or mock.args.generate_client_request:
        request_msg = mock.generate_request_message()
        print(mock.format_message(request_msg))
    elif mock.args.generate_response:
        response_msg = mock.generate_response_message()
        print(mock.format_message(response_msg))
    elif mock.args.send_response:
        mock.send_mock_response()
    elif mock.args.send_request:
        mock.send_mock_request()
    elif mock.args.receive_request:
        mock.receive_request()
    elif mock.args.delete_request:
        receipt_msg = mock.receive_request()
        if receipt_msg is not None:
            receipt, _ = receipt_msg
            mock.delete_request(receipt=receipt)
    elif mock.args.full_life_cycle:
        mock.send_request(message=mock.generate_request_message())
        time.sleep(3)
        receipt = None
        receipt_msg = mock.receive_request()
        if receipt_msg is not None:
            receipt, request_msg = receipt_msg

            response_msg = mock.generate_response_message(message=request_msg)
            mock.send_response(message=response_msg)
            mock.delete_request(receipt=receipt)
