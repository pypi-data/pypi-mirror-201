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

"""Post a task to docuvision API and poll for response."""
from typing import List, Optional, Tuple

import backoff

import hankai.api_client
import hankai.autocoding
import hankai.docuvision
import hankai.lib
import hankai.orchestrator


def main():  # pylint: disable=too-many-locals, disable=too-many-branches, disable=too-many-statements
    """Process a API Client request and receive response."""
    api_client = hankai.api_client.APIClient(  # pylint: disable=unexpected-keyword-arg
        service=None,
        token=None,
        request_message=None,
        api_response_message=None,
        unpicklable=False,
        argparse=True,
        version=hankai.api_client.__version__,
        env=hankai.api_client.APIClientEnv,
    )

    def _format_error_msgs(
        request: hankai.orchestrator.RequestFile,
    ) -> Tuple[str, str]:
        """Format the ErrorTrace message for logging."""
        err_msg: str = ""
        trc_msg: str = ""
        if request.response_error is not None and request.response_error.message:
            err_msg = request.response_error.message
            if (
                request.response_error.tracebacks is not None
                and request.response_error.tracebacks
            ):
                trc_msg = "\n\t".join(request.response_error.tracebacks)

        return (err_msg, trc_msg)

    def _process_response(  # pylint: disable=too-many-branches
        request_file: hankai.orchestrator.RequestFile,
        api_response: hankai.orchestrator.APIResponseMessage,
    ) -> None:
        """Process the response."""
        request_file.set_response_job_id(response_id=api_response.id)

        if api_response.state is hankai.orchestrator.ResponseState.IN_PROGRESS:
            api_client.logenv.logger.debug(
                "Posted request file [{}] job [id={}] received response state [{}]; "
                "continuing.",
                request_file.properties.canonical_path,
                api_response.id,
                api_response.state,
            )
            return

        request_file.response_state = api_response.state
        request_file.response_error = api_response.error

        if api_response.response is None or api_response.response.result is None:
            request_file.response_state = hankai.orchestrator.ResponseState.ERROR
            if not api_response.error:
                request_file.response_error = hankai.orchestrator.ErrorTrace(
                    message=("Response has no result nor error."),
                    tracebacks=None,
                )
            api_client.logenv.logger.critical(
                "Posted request file [{}] job [id={}] has no result. "
                "Origin response state [{}]. Response state set [{}].",
                request_file.properties.canonical_path,
                api_response.id,
                api_response.state,
                request_file.response_state,
            )

        log_message = (
            f"Posted request file [{request_file.properties.canonical_path}] "
            f"job [id={api_response.id}] received response state "
            f"[{request_file.response_state}]."
        )

        if request_file.response_state is hankai.orchestrator.ResponseState.ERROR:
            api_client.logenv.logger.error(log_message)
        else:
            api_client.logenv.logger.info(log_message)
            encoded: str
            extension: Optional[hankai.lib.MimeType] = None
            if not api_client.transformer_inst or api_client.transformer_and_json:
                encoded = api_response.pickle(
                    unpicklable=api_client.unpicklable,
                    redacted=False,
                    indent=2,
                    jsonpickle_handlers=api_response.jsonpickle_handlers(),
                )
                extension = hankai.lib.MimeType(
                    mime_type=hankai.lib.MimeTypeApplication.JSON
                )
                request_file.add_response(
                    encoded=encoded,
                    extension=extension,
                )

            if api_client.transformer_inst:
                transformed_response = api_client.transformer_inst.transform(
                    response=api_response
                )
                if transformed_response is None:
                    raise AssertionError(
                        "Posted request file "
                        f"[{request_file.properties.canonical_path}] "
                        f"job [id={api_response.id}] response result transform "
                        "was unsuccessful."
                    )

                encoded = str(transformed_response)
                extension = None
                transformer_ext = api_client.transformer_inst.filename_extension()
                if transformer_ext is not None:
                    extension = hankai.lib.MimeType.member_by(member=transformer_ext)

                request_file.add_response(
                    encoded=encoded,
                    extension=extension,
                )

            request_file.reconcile()

        request_file.processed = True

    # main() processing start.
    posted_requests: List[
        Tuple[hankai.orchestrator.APIClientExecutor, hankai.orchestrator.RequestFile]
    ] = []
    for request_file in api_client.request_files:
        # Do not let a request that happens to raise an exception stop processing
        # of other request files.
        try:
            req_name = request_file.properties.name
            if api_client.name:
                req_name = api_client.name

            service_family = hankai.orchestrator.ServiceFamilies.family(
                service=api_client.service
            )

            exc_request_message: hankai.orchestrator.SQSRequestMessage
            if service_family is hankai.orchestrator.ServiceFamily.AUTOCODING:
                exc_request_message = api_client.request_message.factory(
                    name=req_name,
                    request_file=request_file.properties,
                    service=api_client.service,
                    api_client=True,
                )
            elif service_family is hankai.orchestrator.ServiceFamily.DOCUVISION:
                exc_request_message = api_client.request_message.factory(
                    name=req_name,
                    request_file=request_file.properties,
                    service=api_client.service,
                    model=api_client.model,
                    confidence_interval=api_client.confidence_interval,
                    perform_ocr=api_client.perform_ocr,
                    api_client=True,
                )

            # Factory performs encode_binary() which sets size and other
            # properties.
            if request_file.properties.size_bytes is None:
                raise AssertionError(
                    f"Request file [{request_file.properties.canonical_path}] "
                    "size bytes is required."
                )

            api_client.logenv.logger.info(
                "Processing requested for file [{}].",
                request_file.properties.canonical_path,
            )

            if api_client.dry_run:
                api_client.logenv.logger.info(
                    "Dry run; POST request file [{}], URI [{}] skipped.",
                    request_file.properties.canonical_path,
                    api_client.uri,
                )
                # Free the request_file encoded data.
                request_file.properties.encoded = None
                continue

            executor = hankai.api_client.APIClientExecutor(
                service=api_client.service,
                token=api_client.token,
                request_message=exc_request_message,
                api_response_message=api_client.api_response_message,
                request_file=request_file,
                logenv=api_client.logenv,
                uri=api_client.uri,
                uri_s3_presigned=api_client.uri_s3_presigned,
                unpicklable=api_client.unpicklable,
                uri_timeout_seconds=api_client.uri_timeout_seconds,
            )

            if (
                request_file.properties.size_bytes
                > api_client.size_bytes_s3_presigned_threshold
            ):
                api_client.logenv.logger.debug(
                    "Request file [{}] size bytes [{}] is greater than the "
                    "threshold size bytes [{}] for AWS Gateway API and requires "
                    "AWS S3 presigned URL.",
                    request_file.properties.canonical_path,
                    request_file.properties.size_bytes,
                    api_client.size_bytes_s3_presigned_threshold,
                )

                executor.post_file_s3_presigned()

                # NOTE! Assure that files large enough must set the request
                # file data to None; if not the API Gateway will likely respond
                # with a 413 status code for 'Entity too large'.
                if isinstance(
                    executor.request_message,
                    hankai.autocoding.AutoCodingSQSRequestMessage,
                ):
                    executor.request_message.request.job = None

                if isinstance(
                    executor.request_message,
                    hankai.docuvision.DocuVisionSQSRequestMessage,
                ):
                    # Currently the Orchestrator/DocuVision API references
                    # the dataKey from request.document.dataKey. Must set
                    # it from the parent hankai.orchestrator.Request class.
                    executor.request_message.request.document.dataKey = (
                        executor.request_message.request.dataKey
                    )
                    executor.request_message.request.document.data = None

            executor.api_response_message = executor.post_request()

            # Free the request_file encoded data.
            request_file.properties.encoded = None

            posted_requests.append(
                (
                    executor,
                    hankai.orchestrator.RequestFile(
                        properties=request_file.properties,
                        logenv=api_client.logenv,
                        processed_directory=api_client.processed_directory,
                        processed_relative=api_client.processed_relative,
                        responses_directory=api_client.responses_directory,
                        responses_relative=api_client.responses_relative,
                        responses_extension_separator=api_client.responses_extension_separator,
                    ),
                )
            )
        except Exception:  # pylint: disable=broad-except
            request_file.response_error = hankai.orchestrator.ErrorTrace(
                message="An exception occurred posting request.",
                tracebacks=hankai.lib.Util.formatted_traceback_exceptions(),
            )
            request_file.response_state = hankai.orchestrator.ResponseState.ERROR
            err_msg, trc_msg = _format_error_msgs(request=request_file)
            api_client.logenv.logger.exception(
                "POST request file [{}] raised an exception. Response state [{}].{}{}",
                request_file.properties.canonical_path,
                request_file.response_state,
                "\n\tError message: " + err_msg if err_msg else "None",
                "\n\tError tracebacks: " + trc_msg if trc_msg else " None",
            )

    @backoff.on_predicate(
        backoff.expo,
        lambda x: x is None,
        max_value=api_client.backoff.max_value_seconds,
        max_time=api_client.backoff.max_time_seconds,
        jitter=backoff.full_jitter,
        logger=None,
    )
    def _get_responses() -> Optional[bool]:  # pylint: disable=too-many-branches
        """Get the responses. Iterate over all posted requests. If there is no
        response for any posted requests backoff checking the API. Return
        True for receiving all posted requests responses. Return True if
        processing timeout exceeded.

        Wrapper for _inner_receive to be able to set @backoff decorator.
        See hankai.lib.Backoff.
        """
        if api_client.dry_run:
            api_client.logenv.logger.info(
                "Dry run; GET response for all request files from URI [{}] " "skipped.",
                api_client.uri,
            )
            return True

        response: Optional[hankai.orchestrator.APIResponseMessage] = None

        received_all = True
        for (executor, request_file) in posted_requests:
            if request_file.processed:
                continue

            received_all = False

            api_client.logenv.logger.debug(
                "Awaiting posted request file [{}] response...",
                request_file.properties.canonical_path,
            )

            # Do not let a request that happens to raise an exception stop processing
            # of other request files.
            try:
                if executor.request_id is None:
                    raise AssertionError(
                        "There is no response id for posted request file "
                        f"[{request_file.properties.canonical_path}]."
                    )
                response = executor.get_response()
                if response is None:
                    raise AssertionError(
                        "There is no response available for "
                        f"job [id={executor.request_id}]."
                    )
                if response:
                    if api_client.logenv.verbosity > 0:
                        api_client.logenv.logger.debug(
                            "Posted request file [{}] response message for "
                            "job [id={}]:\n{}",
                            request_file.properties.canonical_path,
                            executor.request_id,
                            response.pickle(
                                unpicklable=api_client.unpicklable,
                                redacted=True,
                                indent=2,
                                jsonpickle_handlers=response.jsonpickle_handlers(),
                            ),
                        )
                    _process_response(request_file=request_file, api_response=response)
            except Exception:  # pylint: disable=broad-except
                request_file.response_error = hankai.orchestrator.ErrorTrace(
                    message="An exception occurred receiving posted request response.",
                    tracebacks=hankai.lib.Util.formatted_traceback_exceptions(),
                )
                request_file.response_state = hankai.orchestrator.ResponseState.ERROR
                request_file.processed = True

        if received_all:
            return True

        if api_client.timeout_minutes is not None:
            elapsed_minutes = int(
                (hankai.lib.Util.elapsed_seconds(start=start_datetime) / 60)
            )
            if elapsed_minutes >= api_client.timeout_minutes:
                # Set all the un-received responses to ERROR.
                for (_, request_file) in posted_requests:
                    if request_file.processed:
                        continue
                    request_file.response_state = (
                        hankai.orchestrator.ResponseState.ERROR
                    )
                    request_file.response_error = hankai.orchestrator.ErrorTrace(
                        message="Processing timeout minutes "
                        f"[{api_client.timeout_minutes}] exceeded.",
                        tracebacks=None,
                    )

                return False

        # All posted requests responses have not been processed. Triggering backoff.
        return None

    start_datetime = hankai.lib.Util.date_now()

    status = _get_responses()
    if status is False:
        api_client.logenv.logger.critical(
            "Processing exceeded timeout minutes [{}]. Aborting.",
            api_client.timeout_minutes,
        )

    processed: List[hankai.orchestrator.RequestFile] = []
    unprocessed: List[hankai.orchestrator.RequestFile] = []
    for (_, request_file) in posted_requests:
        if request_file.processed:
            processed.append(request_file)
        else:
            unprocessed.append(request_file)

    api_client.logenv.logger.info(
        "Processing completed at [{}] in [{}] seconds for [{}] posted "
        "requests of [{}] total request files.",
        hankai.lib.Util.date_now(),
        hankai.lib.Util.elapsed_seconds(start=start_datetime),
        len(posted_requests),
        len(api_client.request_files),
    )
    if len(processed) != len(posted_requests):
        api_client.logenv.logger.critical(
            "Processed [{}] of [{}] posted requests.",
            len(processed),
            len(posted_requests),
        )

    for request in unprocessed:
        err_msg, trc_msg = _format_error_msgs(request=request)
        api_client.logenv.logger.critical(
            "Unprocessed request file [{}] completed with response state [{}].{}{}",
            request.properties.canonical_path,
            request.response_state,
            "\n\tError message: " + err_msg if err_msg else "",
            "\n\t" + trc_msg if trc_msg else "",
        )

    for request in processed:
        err_msg, trc_msg = _format_error_msgs(request=request)

        if request.response_state is None:
            api_client.logenv.logger.critical(
                "Processed request file [{}] job [id={}] completed with "
                "response state [{}].{}{}",
                request.properties.canonical_path,
                request.get_response_job_id(),
                request.response_state,
                "\n\tError message: " + err_msg if err_msg else "",
                "\n\t" + trc_msg if trc_msg else "",
            )
        elif request.response_state is hankai.orchestrator.ResponseState.ERROR:
            api_client.logenv.logger.error(
                "Processed request file [{}] job [id={}] completed with "
                "response state [{}].{}{}",
                request.properties.canonical_path,
                request.get_response_job_id(),
                request.response_state,
                "\n\tError message: " + err_msg if err_msg else "",
                "\n\t" + trc_msg if trc_msg else "",
            )
        elif request.response_state is hankai.orchestrator.ResponseState.COMPLETED:
            response_files: List[str] = []
            for response in request.responses:
                response_files.append(response.path)

            api_client.logenv.logger.success(
                "Processed request file [{}] job [id={}] completed with "
                "response state [{}].{}{}",
                request.properties.canonical_path,
                request.get_response_job_id(),
                request.response_state,
                "\n\tRelocated: [" + request.processed_destination() + "]",
                "\n\tResponse files: " + "[" + ", ".join(response_files) + "]",
            )
