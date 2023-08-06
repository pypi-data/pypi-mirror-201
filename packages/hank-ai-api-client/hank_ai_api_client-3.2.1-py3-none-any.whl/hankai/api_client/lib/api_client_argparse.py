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
"""DocuVision API Client argument parser."""
import argparse
import os
import textwrap
from argparse import ArgumentParser
from typing import List, Optional

import hankai.autocoding
import hankai.docuvision
import hankai.lib
import hankai.orchestrator

from .api_client_default import APIClientDefault
from .transform import SQSTransform


class APIClientEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and APIClientEnv
    attributes.
    """

    HANK_API_CLIENT_TOKEN = "token"
    HANK_API_CLIENT_SERVICE = "service"
    HANK_API_CLIENT_MODEL = "model"
    HANK_API_CLIENT_NAME = "name"
    HANK_API_CLIENT_CONFIDENCE_INTERVAL = "confidence_interval"
    HANK_API_CLIENT_PERFORM_OCR = "perform_ocr"
    HANK_API_CLIENT_UNPICKLABLE = "unpicklable"
    HANK_API_CLIENT_TIMEOUT_MINUTES = "timeout_minutes"
    HANK_API_CLIENT_URI = "uri"
    HANK_API_CLIENT_URI_S3_PRESIGNED = "uri_s3_presigned"
    HANK_API_CLIENT_URI_TIMEOUT_SECONDS = "uri_timeout_seconds"
    HANK_API_CLIENT_FILES = "files"
    HANK_API_CLIENT_FILES_EXCLUDE_DIRS = "exclude_dirs"
    HANK_API_CLIENT_FILES_EXCLUDE_FILES = "exclude_files"
    HANK_API_CLIENT_FILES_MIME_TYPE = "files_mime_type"
    HANK_API_CLIENT_FILES_ENCODING = "files_encoding"
    HANK_API_CLIENT_FILES_OVERWRITE_EXISTING = "replace_existing_files"
    HANK_API_CLIENT_FILES_REQUESTS_EXTENSION_SEPARATOR_REGEX = (
        "requests_extension_separator_regex"
    )
    HANK_API_CLIENT_FILES_RESPONSES_EXTENSION_SEPARATOR = (
        "responses_extension_separator"
    )
    HANK_API_CLIENT_RESPONSE_TRANSFORMER = "transformer"
    HANK_API_CLIENT_RESPONSE_TRANSFORMER_AND_JSON = "transformer_and_json"
    HANK_API_CLIENT_PROCESSED_DIR = "processed_directory"
    HANK_API_CLIENT_PROCESSED_RELATIVE = "processed_relative"
    HANK_API_CLIENT_RESPONSES_DIR = "responses_directory"
    HANK_API_CLIENT_RESPONSES_RELATIVE = "responses_relative"


class APIClientArgparse(hankai.lib.ArgparseHandler):
    """Create the CLI parser."""

    @staticmethod
    def parser(  # pylint: disable=too-many-statements
        version: Optional[str] = None,
    ) -> ArgumentParser:
        """Return the Argparse Namespace."""
        description = """\
            HANK AI API Client utility and supported transformers for
            processing files. All supported transformers options are
            also listed.
            """

        parser = argparse.ArgumentParser(
            description=textwrap.dedent(description),
            formatter_class=lambda prog: argparse.HelpFormatter(
                prog,
                indent_increment=2,
                max_help_position=10,
                width=80,
            ),
            add_help=False,
        )
        parser.add_argument(
            "--api-token",
            required=not bool(os.getenv(str(APIClientEnv.HANK_API_CLIENT_TOKEN.name))),
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="HANK AI API Client token. "
            "ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_TOKEN.name}].",
        )

        arg_help: List[str] = []
        arg_help.extend(hankai.autocoding.SetService.services_str())
        arg_help.extend(hankai.docuvision.SetService.services_str())

        parser.add_argument(
            "--service",
            required=not bool(
                os.getenv(str(APIClientEnv.HANK_API_CLIENT_SERVICE.name))
            ),
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Request service. One of "
            f"[{'|'.join(arg_help)}]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_SERVICE.name}].",
        )

        arg_help = []
        for service in hankai.orchestrator.Service.members():
            models = hankai.orchestrator.ServiceModel.models_str(service=service)
            if models:
                arg_help.append(f"Service [{service}] one of [{'|'.join(models)}].")

        parser.add_argument(
            "--model",
            required=not bool(os.getenv(str(APIClientEnv.HANK_API_CLIENT_MODEL.name))),
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help=f"Request model. {' '.join(arg_help)} Required for DocuVision "
            f"services. ENV variable [{APIClientEnv.HANK_API_CLIENT_MODEL.name}].",
        )
        parser.add_argument(
            "--files",
            required=False,
            type=str,
            nargs="+",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="One or more relative or absolute paths of document files "
            "and/or directories to process. Directories will be searched "
            f"recursively for requests files. Default {APIClientDefault.files}. "
            f"ENV varible [{APIClientEnv.HANK_API_CLIENT_FILES.name}]. "
            "If ENV variable is defined it must be a Python list. e.g. "
            "['file1.pdf', '/dir1'].",
        )

        arg_help = []
        for service in hankai.orchestrator.Service:
            transforms = SQSTransform.transforms(service=service)
            trns_str: List[str] = []
            for trns in transforms:
                trns_str.append(str(trns))

            if trns_str:
                arg_help.append(f"Service [{service}] one of [{'|'.join(trns_str)}].")

        parser.add_argument(
            "--transformer",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="HANK AI service response message transformer. "
            f"{' '.join(arg_help)} ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_RESPONSE_TRANSFORMER.name}].",
        )
        parser.add_argument(
            "--transformer-and-json",
            required=False,
            action="store_true",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Save the JSON response along with the transformer output. "
            "ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_RESPONSE_TRANSFORMER_AND_JSON.name}].",
        )
        parser.add_argument(
            "--responses-directory",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="A relative or absolute directory path where the responses "
            "will be saved. If relative (e.g. 'responses'), "
            "responses files will be relocated relative to the source. For "
            "example, given a search source path of '/dir1' with a file located "
            "at '/dir1/dir2/file.pdf' responses will be saved at "
            "'/dir1/dir2/responses/file.json' after successful processing. If "
            "absolute (e.g. '/output/responses'), responses will be "
            "saved absolutely replicating the hierarchy beneath the source "
            "path. For example, given a search source path of '/dir1' with a "
            "file located at '/dir1/dir2/file.pdf' the responses will be saved "
            "to '/output/responses/dir2/file.json' after successful processing. "
            "If [--no-relative-responses] and given a relative responses "
            "path (e.g. 'responses') and a source path of '/dir1' and a "
            "file located at '/dir1/dir2/file.pdf' responses will be saved to "
            "'./responses/file.json' the current working directory without the "
            "hierarchy of the source file. If given an absolute path "
            "'/output/responses' and a source path of '/dir1' and "
            "a file located at '/dir1/dir2/file.pdf' responses will be saved to "
            "'/output/responses/file.json' without the hierarchy of the source "
            f"file. Default [{APIClientDefault.responses_directory}]. ENV "
            f"variable [{APIClientEnv.HANK_API_CLIENT_RESPONSES_DIR.name}].",
        )
        parser.add_argument(
            "--no-relative-responses",
            required=False,
            action="store_false",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Responses directory will be absolute. All request document "
            "response results will be saved under the single "
            "[--responses-directory]. CAUTION! If there are documents with the "
            "same name from different paths an exception will be raised for an "
            "already existing name unless [--overwrite-existing-files]. ENV "
            f"variable [{APIClientEnv.HANK_API_CLIENT_RESPONSES_RELATIVE.name}].",
        )
        parser.add_argument(
            "--processed-directory",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="A relative or absolute directory path where the processed "
            "requests will be relocated. If relative (e.g. 'processed'), "
            "processed files will be relocated relative to the source. For "
            "example, given a search source path of '/dir1' with a file located "
            "at '/dir1/dir2/file.pdf' it will be relocated to "
            "'/dir1/dir2/processed/file.pdf' after successful processing. If "
            "absolute (e.g. '/output/processed'), processed files will be "
            "relocated absolutely replicating the hierarchy beneath the source "
            "path. For example, given a search source path of '/dir1' with a "
            "file located at '/dir1/dir2/file.pdf' it will be relocated to "
            "'/output/processed/dir2/file.pdf' after successful processing. If "
            "[--no-relative-processed] and given a relative processed "
            "path (e.g. 'processed') and a source path of '/dir1' and a "
            "file located at '/dir1/dir2/file.pdf' it will be relocated to "
            "'./processed/file.pdf' the current working directory without the "
            "hierarchy of the source file. If given an absolute path "
            "'/output/processed' and a source path of '/dir1' and "
            "a file located at '/dir1/dir2/file.pdf' it will be relocated to "
            "'/output/processed/file.pdf' without the hierarchy of the source "
            f"file. Default [{APIClientDefault.processed_directory}]. ENV "
            f"variable [{APIClientEnv.HANK_API_CLIENT_PROCESSED_DIR.name}].",
        )
        parser.add_argument(
            "--no-relative-processed",
            required=False,
            action="store_false",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Processed request documents will be relocated under the "
            "single [--processed-directory] path. CAUTION! If there are "
            "documents with the same name from different paths an exception "
            "will be raised for an already existing file name unless "
            "[--overwrite-existing-files]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_PROCESSED_RELATIVE.name}].",
        )
        parser.add_argument(
            "--exclude-directories",
            required=False,
            type=str,
            nargs="+",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="One or more directory paths or Python REGEX to exclude from "
            f"requests. Default {APIClientDefault.exclude_dirs}. Relative "
            f"responses directory [{APIClientDefault.responses_directory}] will "
            "be included unless [--no-relative-responses]. Relative processed "
            f"directory [{APIClientDefault.processed_directory}] will "
            f"be included unless [--no-relative-processed]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_FILES_EXCLUDE_DIRS.name}].",
        )
        parser.add_argument(
            "--exclude-files",
            required=False,
            type=str,
            nargs="+",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="One or more file paths or Python REGEX to exclude from "
            f"requests. Default {APIClientDefault.exclude_files}. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_FILES_EXCLUDE_FILES.name}].",
        )
        parser.add_argument(
            "--requests-extension-separator-regex",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Request file name extension separator REGEX pattern. The "
            "REGEX pattern must have 3 groups. Group 1 () before separator, "
            "Group 2 () the separator and Group 3 () the extension. "
            f"Default [{APIClientDefault.requests_extension_separator_regex}]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_FILES_REQUESTS_EXTENSION_SEPARATOR_REGEX.name}].",
        )
        parser.add_argument(
            "--responses-extension-separator",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Responses file name extension separator. "
            f"Default [{APIClientDefault.responses_extension_separator}]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_FILES_RESPONSES_EXTENSION_SEPARATOR.name}].",
        )
        parser.add_argument(
            "--overwrite-existing-files",
            required=False,
            action="store_true",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Overwrite any pre-existing processed request files or response "
            f"files. Default [{APIClientDefault.replace_existing_files}]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_FILES_OVERWRITE_EXISTING.name}].",
        )
        parser.add_argument(
            "--dry-run",
            required=False,
            action="store_true",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Perform a dry run without sending requests or receiving "
            "responses. Default [False].",
        )
        parser.add_argument(
            "--name",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Request message [name]. If provided, all "
            "request messages will use the name in the JSON request message. "
            "Otherwise, the request document name will be utilized for the name. "
            "ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_NAME.name}].",
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
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Document mime type if file unrecognized by libmagic or has "
            "no filename extension. "
            f"{' '.join(arg_help)} Default [{APIClientDefault.mime_type}]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_FILES_MIME_TYPE.name}].",
        )
        parser.add_argument(
            "--encoding",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Encoding base and decoding codec. Format: base/codec. Base "
            f"one of [{'|'.join(hankai.lib.EncodeBinaryBase.members_str())}]. "
            f"Codec one of [{'|'.join(hankai.lib.EncodeStringCodec.members_str())}]. "
            f"Default [{APIClientDefault.encoding}]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_FILES_ENCODING.name}].",
        )
        parser.add_argument(
            "--confidence-interval",
            required=False,
            type=float,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Request confidence interval. Default "
            f"[{APIClientDefault.confidence_interval}]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_CONFIDENCE_INTERVAL.name}].",
        )
        parser.add_argument(
            "--no-perform-ocr",
            required=False,
            action="store_false",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Request processing will not perform OCR. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_PERFORM_OCR.name}].",
        )

        arg_help = []
        for service_family in hankai.orchestrator.ServiceFamily.members():
            uri = hankai.orchestrator.ServiceURI.uri(service_family=service_family)
            arg_help.append(f"service family [{service_family}] uri [{uri}]")

        parser.add_argument(
            "--uri",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help=f"HANK AI API Client URI. Defaults {', '.join(arg_help)}. "
            f"ENV variable [{APIClientEnv.HANK_API_CLIENT_URI.name}].",
        )

        arg_help = []
        for service_family in hankai.orchestrator.ServiceFamily.members():
            uri = hankai.orchestrator.ServiceURI.uri_s3_presigned(
                service_family=service_family
            )
            arg_help.append(
                f"service family [{service_family}] uri s3 presigned [{uri}]"
            )

        parser.add_argument(
            "--uri-s3-presigned",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help=(
                "HANK AI API Client AWS S3 presigned URI. Used to upload "
                "request documents larger than "
                f"[{hankai.orchestrator.APIClientDefault.size_bytes_s3_presigned_threshold}] "
                f"bytes to AWS S3. Defaults {', '.join(arg_help)}. "
                "ENV variable "
                f"[{APIClientEnv.HANK_API_CLIENT_URI_S3_PRESIGNED.name}]."
            ),
        )
        parser.add_argument(
            "--backoff-max-value-seconds",
            required=False,
            type=int,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="HANK AI API Client backoff seconds interval for "
            "checking sent requests processed responses. An integer greater "
            "than zero. Default "
            f"[{hankai.lib.Backoff().max_value_seconds}]. "
            "ENV variable "
            f"[{hankai.lib.BackoffEnv.HANK_BACKOFF_MAX_VALUE_SECONDS.name}].",
        )
        parser.add_argument(
            "--backoff-max-time-seconds",
            required=False,
            type=float,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="HANK AI API Client backoff seconds limit for "
            "checking sent requests processed responses. An float greater "
            "than zero. Default "
            f"[{hankai.lib.Backoff().max_time_seconds}]. "
            "ENV variable "
            f"[{hankai.lib.BackoffEnv.HANK_BACKOFF_MAX_VALUE_SECONDS.name}].",
        )
        parser.add_argument(
            "--timeout-minutes",
            required=False,
            type=int,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="HANK AI API Client timeout minutes limiting the total "
            "request and response processing time. An integer greater than "
            "zero or None. None for no timeout. Default "
            f"[{hankai.orchestrator.APIClientDefault.timeout_minutes}]. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_TIMEOUT_MINUTES.name}].",
        )
        parser.add_argument(
            "--uri-timeout-seconds",
            required=False,
            type=int,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="HANK AI API Client URI timeout seconds limiting the time for "
            "each URI request. An integer greater than zero or None. None for "
            "maximum URI wait time. Default "
            f"[{hankai.orchestrator.APIClientDefault.uri_timeout_seconds}]. "
            "ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_URI_TIMEOUT_SECONDS.name}].",
        )
        parser.add_argument(
            "--log-level",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Loguru level. One of "
            f"[{'|'.join(hankai.lib.LoguruLevel.members_str())}]. "
            f"Default [{str(hankai.lib.LogEnv().log_level)}]. ENV variable "
            f"[{hankai.lib.LogEnvEnv.HANK_LOG_LEVEL.name}].",
        )
        parser.add_argument(
            "--log-syslog",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Loguru SysLog. (host, port): Tuple(Optional[str], int). "
            f"Default [{hankai.lib.LogEnv().log_syslog}]. "
            "ENV variable "
            f"[{hankai.lib.LogEnvEnv.HANK_LOG_SYSLOG.name}].",
        )
        parser.add_argument(
            "--log-file",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help=f"Loguru file path. Default [{hankai.lib.LogEnv().log_file}]. "
            f"ENV variable [{hankai.lib.LogEnvEnv.HANK_LOG_FILE.name}].",
        )
        parser.add_argument(
            "--no-log-stdout",
            required=False,
            action="store_false",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Suppress logging to STDOUT. ENV variable "
            f"[{hankai.lib.LogEnvEnv.HANK_LOG_STDOUT.name}].",
        )
        parser.add_argument(
            "--verbosity",
            required=False,
            type=int,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Verbosity 0 or greater. Default "
            f"[{hankai.lib.LogEnv().verbosity}]. ENV variable "
            f"[{hankai.lib.LogEnvEnv.HANK_VERBOSITY.name}].",
        )
        parser.add_argument(
            "--picklable",
            required=False,
            action="store_true",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Create request as a picklable message. Python class "
            f"annotations are retained. Default [{APIClientDefault.picklable}]; "
            "remove Python class annotations. ENV variable "
            f"[{APIClientEnv.HANK_API_CLIENT_UNPICKLABLE.name}].",
        )
        if version:
            parser.add_argument(
                "--version",
                action="version",
                version=version,
                help="Display version and exit.",
            )

        return parser
