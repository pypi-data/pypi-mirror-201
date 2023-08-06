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
"""HANK API Client argument parser."""
import argparse
import sys
import textwrap
from argparse import Namespace
from typing import List

import hankai.autocoding
import hankai.docuvision
import hankai.lib
import hankai.orchestrator

from .mock_message_default import MockDefault


class MockArgparse:
    """Create the CLI parser."""

    @staticmethod
    def namespace() -> Namespace:
        """Return the Argparse Namespace."""
        description = """\
        This utility will generate mock HANK AI API request messages, response
        messages, send them to their respective queues and delete request
        messages on successful response submission. You must be authenticated
        with AWS.

        For more granular specifications of AWS resources, set ENV variables.
        See: hankai.aws.EnvironmentEnv, hankai.aws.ServicerEnv,
        SQSRequestsEnv and SQSResponsesEnv.

        e.g. hank-ai-api-mock-message --document ANRecord_20210822.pdf
        --generate-client-request
        """
        parser = argparse.ArgumentParser(
            description=textwrap.dedent(description),
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog,
                indent_increment=2,
                max_help_position=10,
                width=80,
            ),
        )
        parser.add_argument(
            "--requests-queue",
            required="--receive-request" in sys.argv
            or "--delete-request" in sys.argv
            or "--full-life-cycle" in sys.argv
            or "--requests-queue-attributes" in sys.argv,
            type=str,
            help="Requests AWS SQS queue name.",
        )
        parser.add_argument(
            "--responses-queue",
            required="--send-response" in sys.argv or "--full-life-cycle" in sys.argv,
            type=str,
            help="Responses AWS SQS queue name.",
        )
        parser.add_argument(
            "--requests-s3-bucket",
            required="--send-request" in sys.argv
            or "--receive-request" in sys.argv
            or "--delete-request" in sys.argv
            or "--full-life-cycle" in sys.argv,
            type=str,
            help="Requests AWS S3 bucket name.",
        )
        parser.add_argument(
            "--responses-s3-bucket",
            required="--send-response" in sys.argv or "--full-life-cycle" in sys.argv,
            type=str,
            help="Responses AWS S3 bucket name.",
        )
        parser.add_argument(
            "--no-s3-always",
            required=False,
            action="store_false",
            help="Do not AWS S3 bucket always for both requests and responses "
            "queues. Default [True] always use S3.",
        )
        parser.add_argument(
            "--document",
            required="--send-response" in sys.argv
            or "--send-request" in sys.argv
            or "--full-life-cycle" in sys.argv
            or "--generate-request" in sys.argv
            or "--generate-client-request" in sys.argv
            or "--generate-response" in sys.argv,
            type=str,
            help="Document to request processing.",
        )
        parser.add_argument(
            "--name",
            required=False,
            type=str,
            help="Request message [name]. If provided, all "
            "request messages will use the name in the JSON request message. "
            "Otherwise, the request document name will be utilized for the name.",
        )

        arg_help: List[str] = []
        arg_help.extend(hankai.autocoding.SetService.services_str())
        arg_help.extend(hankai.docuvision.SetService.services_str())

        parser.add_argument(
            "--service",
            required=True,
            type=str,
            help="Request service. One of " f"[{'|'.join(arg_help)}].",
        )

        arg_help = []
        for service in hankai.orchestrator.Service.members():
            models = hankai.orchestrator.ServiceModel.models_str(service=service)
            if models:
                arg_help.append(f"Service [{service}] one of [{'|'.join(models)}].")

        parser.add_argument(
            "--model",
            required=True,
            type=str,
            help=f"Request model. {' '.join(arg_help)}",
        )

        arg_help = []
        for service in hankai.orchestrator.Service.members():
            mime_types = hankai.orchestrator.MimeType.members_str(service=service)
            if mime_types:
                arg_help.append(f"Service [{service}] one of [{'|'.join(mime_types)}].")

        parser.add_argument(
            "--mime-type",
            required=False,
            type=str,
            help="Document mime type if file extension absent or unrecognized. "
            f"{' '.join(arg_help)} Default [{MockDefault.mime_type}].",
        )
        parser.add_argument(
            "--encoding",
            required=False,
            type=str,
            help="Encoding base and decoding codec. Format: base/codec. Base "
            f"one of [{'|'.join(hankai.lib.EncodeBinaryBase.members_str())}]. "
            f"Codec one of [{'|'.join(hankai.lib.EncodeStringCodec.members_str())}]. "
            f"Default [{MockDefault.encoding}]."
            " ",
        )
        parser.add_argument(
            "--confidence-interval",
            required=False,
            type=float,
            help="Request confidence interval. Default "
            f"[{MockDefault.confidence_interval}].",
        )
        parser.add_argument(
            "--no-perform-ocr",
            required=False,
            default=None,
            action="store_false",
            help="Request processing will not perform OCR. Default "
            f"[{not MockDefault.perform_ocr}]; perform OCR.",
        )
        parser.add_argument(
            "--data-key",
            required=False,
            type=str,
            help="Request document 'dataKey' for AWS S3 presigned.",
        )
        parser.add_argument(
            "--response-state",
            required=False,
            type=str,
            help="Response message state. One of "
            f"[{'|'.join(hankai.orchestrator.ResponseState.members_str())}]. "
            "Default [random pick].",
        )
        parser.add_argument(
            "--no-redact",
            required=False,
            default=None,
            action="store_false",
            help="Do not redact PHI sensitive fields sent to STDOUT. "
            f"Default [{MockDefault.redact}] redact PHI on STDOUT.",
        )

        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            "--send-request",
            action="store_true",
            help="Send request message. Member group [action]. Mutually "
            "exclusive of other [action] group members.",
        )
        group.add_argument(
            "--send-response",
            action="store_true",
            help="Send response message. Member group [action]. Mutually "
            "exclusive of other [action] group members.",
        )
        group.add_argument(
            "--receive-request",
            action="store_true",
            help="Receive request message. Member group [action]. Mutually "
            "exclusive of other [action] group members.",
        )
        group.add_argument(
            "--delete-request",
            action="store_true",
            help="Receive an request message, then delete the request. Member "
            "group [action]. Mutually exclusive of other [action] group "
            "members.",
        )
        group.add_argument(
            "--full-life-cycle",
            action="store_true",
            help="Send request, receive request, send response, delete request. "
            "Member group [action]. Mutually exclusive of other [action] "
            "group members.",
        )
        group.add_argument(
            "--generate-request",
            action="store_true",
            help="Generate a request message and present via STDOUT. Member "
            "group [action]. Mutually exclusive of other [action] "
            "group members.",
        )
        group.add_argument(
            "--generate-client-request",
            action="store_true",
            help="Generate a client request message and present via STDOUT. "
            "Member group [action]. Mutually exclusive of other [action] "
            "group members.",
        )
        group.add_argument(
            "--generate-response",
            action="store_true",
            help="Generate a response message and present via STDOUT. Member "
            "group [action]. Mutually exclusive of other [action] "
            "group members.",
        )
        group.add_argument(
            "--requests-queue-attributes",
            action="store_true",
            help="Get the requests queue attributes and present via "
            "STDOUT. Member group [action]. Mutually exclusive of other "
            "[action] group members.",
        )

        parser.add_argument(
            "--log-level",
            required=False,
            type=str,
            help=f"Loguru level. One of {'|'.join(hankai.lib.LoguruLevel.members_str())}. "
            f"Default [{hankai.lib.LogEnv().log_level}].",
        )
        parser.add_argument(
            "--verbosity",
            "-v",
            required=False,
            action="count",
            help="Verbosity; may be called multiple times. Default "
            f"[{hankai.lib.LogEnv().verbosity}].",
        )
        parser.add_argument(
            "--picklable",
            required=False,
            default=None,
            action="store_true",
            help="Create request as a picklable message. Python class "
            f"annotations are retained. Default [{MockDefault.picklable}]; "
            "remove Python class annotations.",
        )
        parser.add_argument(
            "--version",
            required=False,
            default=None,
            action="store_true",
            help="Display module version and exit. Default [False].",
        )

        return parser.parse_args()
