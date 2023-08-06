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
"""DocuVisionSQSResponseMessage Transformer."""
from __future__ import annotations

import json
import re
from argparse import Namespace
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Type, Union

import pandas  # type: ignore[import]

import hankai.lib
import hankai.orchestrator

from .docuvision_api_response import DocuVisionAPIResponseMessage
from .docuvision_transform_facesheet_csv_default import (
    CSVDefault,
    DotmapValueCI,
    TransformFacesheetClientMap,
    TransformFacesheetMaps,
)
from .docuvision_transform_facesheet_csv_parser import TransformFacesheetCSVParser
from .enum_other import PhoneNumberFormat


@dataclass
class TransformFacesheetCSV(
    hankai.orchestrator.APIResponseTransform
):  # pylint:disable=too-many-instance-attributes
    """Transform AWS SQS response message JSON to CSV format.

    https://www.geeksforgeeks.org/convert-json-to-facesheet-csv-in-python/
    """

    logenv: hankai.lib.LogEnv
    sort_columns: bool = CSVDefault.sort_columns
    separator: str = CSVDefault.separator
    na_representation: str = CSVDefault.na_representation
    float_format: Optional[str] = CSVDefault.float_format
    index: bool = CSVDefault.index
    index_label: Optional[Union[str, bool]] = CSVDefault.index_label
    quote_char: str = CSVDefault.quote_char
    line_terminator: str = CSVDefault.line_terminator
    date_format: Optional[str] = CSVDefault.date_format
    double_quote: bool = CSVDefault.double_quote
    escape_char: Optional[str] = CSVDefault.escape_char
    decimal: str = CSVDefault.decimal
    filename_ext: str = hankai.lib.MimeTypeText.CSV.ext
    phone_region: str = CSVDefault.phone_region
    phone_format: Optional[PhoneNumberFormat] = CSVDefault.phone_format
    client_map_file: Optional[str] = CSVDefault.client_map_file
    client_labels_maps: Optional[List[TransformFacesheetClientMap]] = None
    cli_args: Optional[Namespace] = None
    env: Optional[Type[hankai.lib.EnvEnum]] = None

    def __post_init__(self) -> None:
        if self.env:
            self.logenv.env_supersede(clz=self, env_type=self.env)

        self._argparse(cli_args=self.cli_args)

        if self.client_map_file:
            self._init_client_map()

        self.csv_maps = TransformFacesheetMaps()

    def _init_client_map(self) -> None:
        """Initialize the client_labels_maps from client map file.

        Forms allowed:
        client_column: null
        client_column: [dotmap_name]
        client_column: {"maps": [dotmap_name]}
        client_column: {"maps": [dotmap_name], "na": "na-value"}

        {
            "Location Identifier": {
                "maps": [
                    "LocationFacility"
                ]
            },
            "Location Identifier2": [
                "LocationFacility"
            ],
            "Patient SSN": null,
            "Visit Number (Hospital Account Number)": {
                "maps": [
                    "PatientACCN"
                ],
                "na": "default"
            }
        }
        """
        if not self.client_map_file:
            return

        client_labels_maps = json.loads(
            hankai.lib.Sys.read_file(file=self.client_map_file),
        )
        self.client_labels_maps = []
        for column, maps_na in client_labels_maps.items():
            if maps_na is None:
                self.client_labels_maps.append(
                    TransformFacesheetClientMap(
                        column=column,
                        maps=None,
                        na=None,
                    )
                )
                continue

            if isinstance(maps_na, List):
                self.client_labels_maps.append(
                    TransformFacesheetClientMap(
                        column=column,
                        maps=maps_na,
                        na=None,
                    )
                )
                continue

            if not isinstance(maps_na, dict):
                raise AssertionError(
                    "Invalid transform mapping for client map file "
                    f"[{self.client_map_file}]."
                )

            maps = maps_na.get("maps")
            na = maps_na.get("na")  # pylint: disable=invalid-name
            if maps is None or not isinstance(maps, List):
                raise AssertionError(
                    f"Invalid transform mapping. Client column [{column}] "
                    "requires [maps] list."
                )

            if na is not None and not isinstance(na, str):
                raise AssertionError(
                    f"Invalid transform mapping. Client column [{column}] "
                    "optionally provided [na] must be a string."
                )

            self.client_labels_maps.append(
                TransformFacesheetClientMap(
                    column=column,
                    maps=maps,
                    na=na,
                )
            )

    def filename_extension(self) -> Optional[str]:
        """Return CSV transform filename extension."""
        return self.filename_ext

    def transform(  # pylint: disable=too-many-locals, disable=too-many-branches, disable=too-many-statements
        self,
        response: DocuVisionAPIResponseMessage,
    ) -> Optional[str]:
        """Transform the AWS SQS response message JSON to CSV format."""
        if not isinstance(response, DocuVisionAPIResponseMessage):
            raise AssertionError(
                "Argument [response] must be DocuVisionAPIResponseMessage."
            )
        if (
            response.response is None
            or response.response.result is None
            or response.response.result.RESULT is None
        ):
            raise AssertionError("API response result and RESULT are required.")

        dotmap: str
        value: str
        confidence: float

        result_df = pandas.DataFrame(response.response.result.RESULT)
        group_df = result_df.groupby(by=self.csv_maps.group_by, sort=False)[
            self.csv_maps.group_by_select
        ]

        # First collect all labels that are present in the results. This is to assist
        # in creating DataFrames of the same dimension. Pre-create the synthetic *Name
        # and *Address dotmaps if the native *Name or *Address dotmap appears in the
        # collection.
        all_dotmaps: Set[str] = set()
        for group in group_df:
            page_df = group[1]
            for _, items in page_df.iterrows():
                _, _, dotmap, _, _ = items
                if dotmap.endswith(self.csv_maps.parse_names):
                    all_dotmaps.add(dotmap)
                    for label in self.csv_maps.syn_names:
                        all_dotmaps.add(dotmap + label)
                elif dotmap.endswith(self.csv_maps.parse_addresses):
                    all_dotmaps.add(dotmap)
                    for label in self.csv_maps.syn_addresses:
                        all_dotmaps.add(dotmap + label)
                else:
                    all_dotmaps.add(dotmap)

        # Assure DateProcessed is added to all dotmaps. It is synthetic and
        # is not produced by the processor.
        all_dotmaps.add(self.csv_maps.syn_date_processed)

        # Sort the dotmaps, lengthiest to shortest; highest specificity to least.
        sorted_all_dotmaps: List[str] = sorted(all_dotmaps, key=len, reverse=True)

        dotmap_value: DotmapValueCI
        aggregate_data_frame = pandas.DataFrame()

        # Note! This code block is reliant on Group By "pid"".
        for group in group_df:  # pylint: disable=too-many-nested-blocks
            pid, page_df = group
            dotmap_value = DotmapValueCI(
                na_representation=self.na_representation,
            )

            # Add synthetic DateProcessed.
            if (
                response.response.metadata is not None
                and response.response.metadata.processEndTime is not None
            ):
                processed_date: str
                if self.date_format is not None:
                    processed_date = response.response.metadata.processEndTime.strftime(
                        self.date_format
                    )
                else:
                    processed_date = (
                        response.response.metadata.processEndTime.isoformat()
                    )

                dotmap_value.add(
                    dotmap=self.csv_maps.syn_date_processed,
                    value=processed_date,
                    confidence=0.99,
                )

            for _, items in page_df.iterrows():
                page_num, pid, dotmap, value, confidence = items

                # Panda's may return 'nan' for the value where the type(value)
                # is not a string. This is extreme and it is not possible to
                # discern a value.
                if not isinstance(value, str):
                    if self.logenv.verbosity > 1:  # type: ignore[unreachable]
                        self.logenv.logger.warning(
                            "OriginDocumentPage [{}] PID [{}] dotmap [{}] "
                            "encountered a NaN value [{}]. "
                            "This PID and dotmap will be ignored.",
                            page_num,
                            pid,
                            dotmap,
                            value,
                        )
                    continue

                parser = TransformFacesheetCSVParser(
                    dotmap_value_ci=dotmap_value,
                    page_num=page_num,
                    pid=pid,
                    dotmap=dotmap,
                    value=value,
                    confidence=confidence,
                    na_representation=self.na_representation,
                    phone_region=self.phone_region,
                    phone_format=self.phone_format,
                    logenv=self.logenv,
                )
                parsed_addr = parser.address()
                parsed_name = parser.names()
                parsed_phone = parser.phones()
                if not parsed_addr and not parsed_name and not parsed_phone:
                    dotmap_value.add(
                        dotmap=dotmap,
                        value=value,
                        confidence=confidence,
                    )
                del parser

            # Pack the page for equal dimensions and map client labels to
            # Facesheet dotmaps.
            datetime_regex = re.compile(r".*(date|time|dob).*", re.IGNORECASE)
            datetime_columns: Set[str] = set()
            page_packed: Dict[str, List[str]] = {}

            if self.client_labels_maps is None:
                for dotmap in sorted_all_dotmaps:
                    if self.date_format and datetime_regex.match(dotmap):
                        datetime_columns.add(dotmap)

                    page_packed[dotmap] = []
                    page_packed[dotmap].append(
                        dotmap_value.value(
                            dotmap=dotmap,
                            na_representation=self.na_representation,
                            join=", ",
                        )
                    )
            else:
                for clm in self.client_labels_maps:
                    column = clm.column
                    maps = clm.maps
                    na_rep = clm.na  # pylint: disable=invalid-name

                    if na_rep is None:
                        na_rep = self.na_representation

                    page_packed[column] = []

                    if maps is None:
                        page_packed[column].append(self.na_representation)
                        continue

                    matched: bool = False
                    for hank_dotmap in maps:
                        regex = re.compile(rf".*{hank_dotmap}$")
                        for dotmap in list(filter(regex.match, sorted_all_dotmaps)):
                            if self.date_format and datetime_regex.match(dotmap):
                                datetime_columns.add(column)

                            if dotmap_value.values(dotmap=dotmap):
                                page_packed[column].append(
                                    dotmap_value.value(
                                        dotmap=dotmap,
                                        na_representation=na_rep,
                                        join=", ",
                                    )
                                )
                                matched = True
                                break
                        if matched:
                            break

                    if not matched:
                        page_packed[column].append(na_rep)

            # Sort on column names, concat the DataFrames and reset the index.
            page_packed_df: pandas.DataFrame
            if self.sort_columns:
                page_packed_df = pandas.DataFrame(page_packed).sort_index(axis=1)
            else:
                page_packed_df = pandas.DataFrame(page_packed)

            aggregate_data_frame = pandas.concat(
                [aggregate_data_frame, page_packed_df]
            ).reset_index(drop=True)

            # Set known datetime columns to specific date type prior to calling
            # to_csv() to allow to_csv date_format to apply.
            if self.date_format:
                for dcol in datetime_columns:
                    aggregate_data_frame[dcol] = pandas.to_datetime(
                        aggregate_data_frame[dcol],
                        errors="coerce",
                    )

            del datetime_columns
            del page_packed_df
            del page_packed
            del dotmap_value

        # Not all options exposed; header, encoding, compression, etc.
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
        return aggregate_data_frame.to_csv(  # type: ignore[no-any-return]
            sep=self.separator,
            na_rep=self.na_representation,
            float_format=self.float_format,
            index=self.index,
            index_label=self.index_label,
            quotechar=self.quote_char,
            lineterminator=self.line_terminator,
            date_format=self.date_format,
            doublequote=self.double_quote,
            escapechar=self.escape_char,
            decimal=self.decimal,
        )

    def _argparse(  # pylint: disable=too-many-branches, disable=too-many-statements
        self,
        cli_args: Optional[Namespace],
    ) -> None:
        """Reconcile the CLI arguments and potentially overridden ENV variables.
        CLI arguments supersede any ENV superseded variables.
        """
        if cli_args is None:
            return

        args = vars(cli_args)
        for arg in args:
            if args[arg] == hankai.lib.Argparse.NOT_PROVIDED:
                continue

            val = args[arg]

            if arg == "facesheet_csv_client_map_file" and val:
                self.client_map_file = val

            if arg == "facesheet_csv_phone_region" and val:
                self.phone_region = val

            if arg == "facesheet_csv_phone_format" and val:
                self.phone_format = val
                obj = hankai.lib.Util.objectify(
                    value=val,
                    type_hint=PhoneNumberFormat,
                )
                if obj is not None:
                    self.phone_format = obj

            if arg == "facesheet_csv_sort_columns":
                self.sort_columns = val

            if arg == "facesheet_csv_separator" and len(val) == 1:
                self.separator = val

            if arg == "facesheet_csv_na_representation":
                self.na_representation = val

            if arg == "facesheet_csv_float_format":
                obj = hankai.lib.Util.objectify(
                    value=val,
                    type_hint=Optional[str],
                )
                self.float_format = obj

            if arg == "facesheet_csv_include_index":
                self.index = val

            if arg == "facesheet_csv_index_label":
                obj = hankai.lib.Util.objectify(
                    value=val,
                    type_hint=Optional[Union[str, bool]],
                )
                self.index_label = obj

            if arg == "facesheet_csv_quote_char" and len(val) == 1:
                self.quote_char = val

            if arg == "facesheet_csv_line_terminator" and val:
                self.line_terminator = val

            if arg == "facesheet_csv_date_format":
                obj = hankai.lib.Util.objectify(
                    value=val,
                    type_hint=Optional[str],
                )
                self.date_format = obj

            if arg == "facesheet_csv_no_double_quote":
                self.double_quote = val

            if arg == "facesheet_csv_escape_char":
                obj = hankai.lib.Util.objectify(
                    value=val,
                    type_hint=Optional[str],
                )
                self.escape_char = obj

            if arg == "facesheet_csv_decimal" and val:
                self.decimal = val

            if arg == "facesheet_csv_filename_ext":
                self.filename_ext = val
