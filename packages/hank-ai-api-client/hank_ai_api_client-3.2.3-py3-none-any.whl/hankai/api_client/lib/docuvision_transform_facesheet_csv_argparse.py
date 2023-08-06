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
import textwrap
from argparse import ArgumentParser
from typing import Optional

import hankai.docuvision
import hankai.lib
import hankai.orchestrator

from .docuvision_transform_facesheet_csv_default import CSVDefault
from .enum_other import PhoneNumberFormat


class TransformFacesheetCSVEnv(hankai.lib.EnvEnum):
    """Convenience class of ENV variables and SimpleQueueServiceEnv attributes.

    NOTE! Multiple applications, utilizing the hank-ai-* Python packages,
    running concurrently may and likely should define their own EnvEnum and
    pass to the class [env] attribute. Providing a unique set of EnvEnum
    assures that each application can define different values for the same
    attribute.
    """

    HANK_TRANSFORM_FACESHEET_CSV_SORT_COLUMNS = "sort_columns"
    HANK_TRANSFORM_FACESHEET_CSV_SEPARATOR = "separator"
    HANK_TRANSFORM_FACESHEET_CSV_NA_REP = "na_representation"
    HANK_TRANSFORM_FACESHEET_CSV_FLOAT_FORMAT = "float_format"
    HANK_TRANSFORM_FACESHEET_CSV_INDEX = "index"
    HANK_TRANSFORM_FACESHEET_CSV_INDEX_LABEL = "index_label"
    HANK_TRANSFORM_FACESHEET_CSV_QUOTE_CHAR = "quote_char"
    HANK_TRANSFORM_FACESHEET_CSV_LINE_TERMINATOR = "line_terminator"
    HANK_TRANSFORM_FACESHEET_CSV_DATE_FORMAT = "date_format"
    HANK_TRANSFORM_FACESHEET_CSV_DOUBLE_QUOTE = "double_quote"
    HANK_TRANSFORM_FACESHEET_CSV_ESCAPER_CHAR = "escape_char"
    HANK_TRANSFORM_FACESHEET_CSV_DECIMAL = "decimal"
    HANK_TRANSFORM_FACESHEET_CSV_FILENAME_EXT = "filename_ext"
    HANK_TRANSFORM_FACESHEET_CSV_PHONE_REGION = "phone_region"
    HANK_TRANSFORM_FACESHEET_CSV_PHONE_FORMAT = "phone_format"
    HANK_TRANSFORM_FACESHEET_CSV_CLIENT_MAP_FILE = "client_map_file"


class TransformFacesheetCSVArgparse(hankai.lib.ArgparseHandler):
    """Create the CLI parser."""

    @staticmethod
    def parser(version: Optional[str] = None) -> ArgumentParser:
        """Return the Argparse Namespace."""

        description = """\
            Transformer - DocuVision Facesheet CSV -----------------------------
            Transform DocuVision Facesheet JSON responses to CSV.
            Optional arguments begin with --facesheet-csv- and are
            listed below. It utilizes the Python Pandas modules
            pandas.DataFrame.sort_values and pandas.DataFrame.to_csv.

            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html
            https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html
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
            "--facesheet-csv-client-map-file",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Client labels Facesheet mappings JSON. Default "
            f"[{CSVDefault.client_map_file}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_CLIENT_MAP_FILE.name}]. "
            "e.g."
            """\
    {
        "Location Identifier": [
            "LocationFacility"
        ],
        "Visit Number (Hospital Account Number)": {
            "maps": [
                "PatientACCN"
            ]
        },
        "Visit History Number (Medical Record Number)": {
            "maps": [
                "PatientMRN"
            ],
            "na": "default"
        },
        "Visit Type / Status": [
            "AdmStatusInpatient",
            "AdmStatusObservation",
            "AdmStatusOutpatient"
        ]
    }""",
        )
        parser.add_argument(
            "--facesheet-csv-phone-region",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="Phone region. See "
            "https://github.com/daviddrysdale/python-phonenumbers. Default "
            f"[{CSVDefault.phone_region}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_PHONE_REGION.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-phone-format",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help=f"Phone region. One of [{'|'.join(PhoneNumberFormat.members_str())}]. "
            "See https://github.com/daviddrysdale/python-phonenumbers. Default "
            f"[{CSVDefault.phone_format}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_PHONE_FORMAT.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-sort-columns",
            required=False,
            action="store_true",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help=f"Sort the columns. Default [{CSVDefault.sort_columns}]. ENV "
            "variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_SORT_COLUMNS.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-separator",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help=f"CSV field delimiter. Default [{CSVDefault.separator}]. ENV "
            "variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_SEPARATOR.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-na-representation",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV missing data representation. Default "
            f"[{CSVDefault.na_representation}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_NA_REP.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-float-format",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV format string for floating point numbers. Default "
            f"[{CSVDefault.float_format}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_FLOAT_FORMAT.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-include-index",
            required=False,
            action="store_true",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help=f"CSV include index column. Default  [{CSVDefault.index}]. ENV "
            "variable [HANK_TRANSFORM_FACESHEET_CSV_INDEX].",
        )
        parser.add_argument(
            "--facesheet-csv-index-label",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV index label if index is included. String, False or None. "
            f"Default [{CSVDefault.index_label}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_INDEX_LABEL.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-quote-char",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV character used to quote fields. Default "
            f"[{CSVDefault.quote_char}]. ENV variable "
            "[HANK_TRANSFORM_FACESHEET_CSV_QUOTE_CHAR].",
        )
        parser.add_argument(
            "--facesheet-csv-no-double-quote",
            required=False,
            action="store_false",
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV control quoting of [--quote-char] inside a field. ENV "
            "variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_DOUBLE_QUOTE.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-line-terminator",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV newline character or character sequence to use in the "
            f"output. Default [{CSVDefault.line_terminator}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_LINE_TERMINATOR.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-date-format",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV format string for the datetime objects. Format follows "
            "the Python datetime strftime(). Default "
            f"[{CSVDefault.date_format}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_DATE_FORMAT.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-escape-char",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV character used to escape [--separator] and [--quote-char] "
            f"when appropriate. Default [{CSVDefault.escape_char}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_ESCAPER_CHAR.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-decimal",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV character recognized as decimal separator. Default "
            f"[{CSVDefault.decimal}]. ENV variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_DECIMAL.name}].",
        )
        parser.add_argument(
            "--facesheet-csv-filename-ext",
            required=False,
            type=str,
            default=hankai.lib.Argparse.NOT_PROVIDED,
            help="CSV filename extension. Set with '' for eliminating the "
            f"filename extension. Default [{CSVDefault.filename_ext}]. ENV "
            "variable "
            f"[{TransformFacesheetCSVEnv.HANK_TRANSFORM_FACESHEET_CSV_FILENAME_EXT.name}].",
        )

        return parser
