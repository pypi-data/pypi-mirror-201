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
"""Post a task to docuvision API and poll for response."""
import os
import textwrap
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Type

import hankai.autocoding
import hankai.docuvision
import hankai.lib
import hankai.orchestrator

from .api_client_argparse import APIClientArgparse
from .api_client_default import APIClientDefault
from .autocoding_api_response import AutoCodingAPIResponseMessage
from .docuvision_api_response import DocuVisionAPIResponseMessage
from .transform import ServiceTransform, SQSTransform


@dataclass
class APIClient(
    hankai.orchestrator.APIClient
):  # pylint: disable=too-many-instance-attributes
    """Create the DocuVision request message and process the response.
    Command line options via Argparse will supersede ENV variables. While
    [request_message], [response_message] and [api_response_message] are
    optional for instantiating the class, they will be set to the [service]
    defaults if they are not assigned a value at instantiation.
    """

    files: List[str] = field(default_factory=lambda: APIClientDefault.files)
    request_message: Optional[hankai.orchestrator.SQSRequestMessage] = None
    api_response_message: Optional[hankai.orchestrator.APIResponseMessage] = None
    transformer_inst: Optional[hankai.orchestrator.APIResponseTransform] = None
    transformer: Optional[ServiceTransform] = None
    transformer_and_json: bool = False
    responses_directory: str = APIClientDefault.responses_directory
    responses_relative: bool = APIClientDefault.responses_relative
    processed_directory: str = APIClientDefault.processed_directory
    processed_relative: bool = APIClientDefault.processed_relative
    exclude_dirs: List[str] = field(
        default_factory=lambda: APIClientDefault.exclude_dirs
    )
    exclude_files: List[str] = field(
        default_factory=lambda: APIClientDefault.exclude_files
    )
    requests_extension_separator_regex: str = (
        APIClientDefault.requests_extension_separator_regex
    )
    responses_extension_separator: str = APIClientDefault.responses_extension_separator
    replace_existing_files: bool = APIClientDefault.replace_existing_files
    dry_run: bool = False
    files_encoding: hankai.lib.Encoding = APIClientDefault.encoding
    model: Optional[hankai.orchestrator.Model] = None
    files_mime_type: hankai.lib.MimeType = APIClientDefault.mime_type
    confidence_interval: float = APIClientDefault.confidence_interval
    perform_ocr: bool = APIClientDefault.perform_ocr

    # ---
    argparse: bool = False
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        self.request_files: List[hankai.orchestrator.RequestFile] = []
        self.cli_args: Optional[Namespace] = None

        # _argparse will be composed of all the potential transformer options
        # in cli_args.
        if self.argparse:
            self.cli_args = self._argparse()

        self._validate_options()

        # Wait to call super until ENV supersedes and CLI argparse have an
        # opportunity to set required fields.
        super().__post_init__()
        self._check_and_set_paths(src_items=self._load_files())

    def _validate_options(self) -> None:  # pylint: disable=too-many-branches
        """Validate the options."""
        service_family = hankai.orchestrator.ServiceFamilies.family(
            service=self.service
        )

        if self.transformer:
            sqs_transform = SQSTransform.transformer(
                service=self.service, transform=self.transformer
            )
            if sqs_transform is None:
                raise ValueError(
                    f"Option [--transformer={self.transformer}] is "
                    f"not supported for service [{self.service}]."
                )

            # Instantiate the transformer and optional argparse.
            response_transform_path = (
                sqs_transform.api_response_transform.__module__
                + "."
                + sqs_transform.api_response_transform.__name__
            )
            module_name, cls = hankai.lib.Util.class_by_hint(
                type_str=response_transform_path,
            )
            if module_name is None or cls is None:
                raise AssertionError(
                    f"Transformer [{sqs_transform.api_response_transform}] "
                    "could not be found."
                )

            self.transformer_inst = cls(
                logenv=self.logenv,
                cli_args=self.cli_args,
                env=sqs_transform.env,
            )

        # Adjust the messages.
        if service_family is hankai.orchestrator.ServiceFamily.AUTOCODING:
            if self.request_message is None:
                self.request_message = hankai.autocoding.AutoCodingSQSRequestMessage()
            if self.api_response_message is None:
                self.api_response_message = AutoCodingAPIResponseMessage()

            # Unset options which do not apply to DocuVision.
            del self.model
            del self.files_mime_type
            del self.confidence_interval
            del self.perform_ocr
        elif service_family is hankai.orchestrator.ServiceFamily.DOCUVISION:
            if self.request_message is None:
                self.request_message = hankai.docuvision.DocuVisionSQSRequestMessage()
            if self.api_response_message is None:
                self.api_response_message = DocuVisionAPIResponseMessage()

            # Model.
            if self.model is None or not hankai.orchestrator.ServiceModel.supported(
                service=self.service, model=self.model
            ):
                raise ValueError(
                    f"Model [{self.model}] is not supported for DocuVision "
                    f"service [{self.service}]."
                )

            # MimeType.
            if not hankai.orchestrator.MimeType.supported(
                service=self.service, mime_type=self.files_mime_type
            ):
                raise ValueError(
                    f"MimeType [{self.files_mime_type}] is not supported for DocuVision "
                    f"service [{self.service}]."
                )

            # Confidence interval max/min.
            self.confidence_interval = hankai.orchestrator.ConfidenceInterval.normalize(
                confidence=self.confidence_interval
            )

        if self.request_message is None or self.api_response_message is None:
            raise ValueError(
                "Argument [request_message] and [api_response_message] are required."
            )

    def _load_files(self) -> hankai.lib.SourceItems:
        """Collect the documents for processing."""

        if self.processed_relative and not os.path.isabs(self.processed_directory):
            self.exclude_dirs.append(self.processed_directory)
        if self.responses_relative and not os.path.isabs(self.responses_directory):
            self.exclude_dirs.append(self.responses_directory)

        src_items = hankai.lib.SourceItems(
            paths=self.files,
            exclude_dirs=self.exclude_dirs,
            exclude_files=self.exclude_files,
            recursive=True,
        )

        return src_items

    def _check_and_set_paths(self, src_items: hankai.lib.SourceItems) -> None:
        """Check and set the request documents paths."""
        # Assert responses and processed directories are directories; create
        # if non existent.
        for item in src_items.items():
            for file in item.included_files():
                request_file_properties = hankai.lib.FileProperties(
                    path=file,
                    source_path=item.source_path(),
                    encoding=self.files_encoding,
                )

                request_file = hankai.orchestrator.RequestFile(
                    properties=request_file_properties,
                    logenv=self.logenv,
                    processed_directory=self.processed_directory,
                    processed_relative=self.processed_relative,
                    responses_directory=self.responses_directory,
                    responses_relative=self.responses_relative,
                    responses_extension_separator=self.responses_extension_separator,
                )

                # If mime_type could not be inferred, set to the default files_mime_type.
                if request_file.properties.mime_type is None and self.files_mime_type:
                    request_file.properties.mime_type = self.files_mime_type

                self.request_files.append(request_file)

    # pylint: disable=too-many-branches, disable=too-many-statements, disable=too-many-locals
    def _argparse(self) -> Namespace:
        """Reconcile the CLI arguments and potentially overridden ENV variables.
        CLI arguments supersede any ENV superseded variables.
        """
        self.logenv.set_log_format(pattern=self.log_format)
        api_client_argparser = APIClientArgparse.parser(version=self.version)

        # Create composite argparse containing the 'parent' APIClientArgparse
        # and all the supported transformers.
        child_parsers: List[ArgumentParser] = [api_client_argparser]
        child_descriptions: List[str] = []
        if api_client_argparser.description:
            child_descriptions.append(api_client_argparser.description)

        for argparser in SQSTransform.unique_api_response_transform_argparsers():
            argparser_path = argparser.__module__ + "." + argparser.__name__
            _, cls = hankai.lib.Util.class_by_hint(
                type_str=argparser_path,
            )
            if cls is None:
                raise AssertionError(
                    f"Transform argparse class [{argparser_path}] could not "
                    "be found."
                )
            child_parser = cls().parser()
            child_parsers.append(child_parser)
            if child_parser.description:
                child_descriptions.append(child_parser.description)

        composite_argparser = ArgumentParser(
            description=textwrap.dedent("\n".join(child_descriptions)),
            formatter_class=lambda prog: RawDescriptionHelpFormatter(
                prog,
                indent_increment=2,
                max_help_position=10,
                width=80,
            ),
            parents=child_parsers,
        )

        cli_args = composite_argparser.parse_args()
        args = vars(cli_args)

        for arg in args:
            if args[arg] == hankai.lib.Argparse.NOT_PROVIDED:
                continue

            val = args[arg]

            # Check loguru and verbosity first for subsequent logging actions.
            if arg == "log_level":
                log_level = hankai.lib.LoguruLevel.member_by(val)
                if log_level is None:
                    raise ValueError(f"Option [--log-level={val}] is not supported.")
                self.logenv.set_log_level(log_level)

            if arg == "verbosity":
                self.logenv.set_verbosity(val)

            if arg == "log_syslog":
                address: Optional[
                    Tuple[Optional[str], int]
                ] = hankai.lib.Util.objectify(
                    value=val,
                    type_hint=Tuple[Optional[str], int],
                    is_json=False,
                )
                if address is not None:
                    self.logenv.set_log_syslog(address=address)

            if arg == "log_file" and val:
                self.logenv.set_log_file(path=val)

            if arg == "no_log_stdout":
                self.logenv.set_log_stdout(enable=val)

            if arg == "api_token" and val:
                self.token = val

            if arg == "service":
                service: Optional[
                    hankai.orchestrator.Service
                ] = hankai.orchestrator.Service.member_by(val)
                if service is None:
                    raise ValueError(f"Option [--service={val}] is not supported.")
                self.service = service

            if arg == "files" and val:
                self.files = val

            if arg == "transformer" and val:
                service_transform = ServiceTransform.member_by(member=val)
                if not service_transform:
                    raise ValueError(f"Option [--transformer={val}] is not supported.")
                self.transformer = service_transform

            if arg == "transformer_and_json":
                self.transformer_and_json = val

            if arg == "responses_directory" and val:
                self.responses_directory = val

            if arg == "no_relative_responses":
                self.responses_relative = val

            if arg == "processed_directory" and val:
                self.processed_directory = val

            if arg == "no_relative_processed":
                self.processed_relative = val

            if arg == "exclude_directories":
                self.exclude_dirs = val

            if arg == "exclude_files":
                self.exclude_files = val

            if arg == "requests_extension_separator_regex":
                self.requests_extension_separator_regex = val

            if arg == "responses_extension_separator":
                self.responses_extension_separator = val

            if arg == "replace_existing_files":
                self.replace_existing_files = val

            if arg == "dry_run":
                self.dry_run = val

            if arg == "name":
                self.name = val

            if arg == "uri" and val:
                self.uri = str(val)

            if arg == "uri_s3_presigned" and val:
                self.uri_s3_presigned = str(val)

            if arg == "backoff_max_value_seconds":
                self.backoff.max_value_seconds = int(val)
                self.backoff.set_floor()

            if arg == "backoff_max_time_seconds":
                self.backoff.max_time_seconds = float(val)
                self.backoff.set_floor()

            if arg == "timeout_minutes":
                self.timeout_minutes = val

            if arg == "uri_timeout_seconds":
                self.uri_timeout_seconds = val

            if arg == "picklable":
                self.unpicklable = val

            if arg == "confidence_interval":
                self.confidence_interval = val

            if arg == "no_perform_ocr":
                self.perform_ocr = val

            if arg == "encoding":
                files_encoding = hankai.lib.Encoding.unpicklable(val)
                if not files_encoding:
                    raise ValueError(f"Option [--encoding={val}] is not supported")
                self.files_encoding = files_encoding

            if arg == "model":
                self.model = hankai.orchestrator.Model.member_by(val)
                if not self.model:
                    raise ValueError(f"Option [--model={val}] is not supported.")
                if not hankai.orchestrator.ServiceModel.supported(
                    service=self.service, model=self.model
                ):
                    raise ValueError(
                        f"Option [--model={val}] is not supported for service [{self.service}]."
                    )

            if arg == "mime_type":
                files_mime_type = hankai.lib.MimeType.member_by(val)
                if not files_mime_type:
                    raise ValueError(f"Option [--mime-type={val}] is not supported.")
                if not hankai.orchestrator.MimeType.supported(
                    service=self.service, mime_type=files_mime_type
                ):
                    raise ValueError(
                        f"Option [--mime-type={val}] is not supported for service [{self.service}]."
                    )
                self.files_mime_type = files_mime_type

        return cli_args
