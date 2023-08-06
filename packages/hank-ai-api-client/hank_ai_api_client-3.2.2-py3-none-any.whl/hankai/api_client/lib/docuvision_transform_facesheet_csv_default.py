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
"""DocuVision API Client defaults."""
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import hankai.lib
import hankai.orchestrator

from .enum_other import PhoneNumberFormat


class CSVDefault:  # pylint: disable=too-many-instance-attributes
    """DocuVision API Client defaults."""

    sort_by: Union[str, List[str]] = []
    sort_ascending: Union[bool, List[bool]] = True
    sort_columns: bool = False
    separator: str = ","
    na_representation: str = ""
    float_format: Optional[str] = None
    index: bool = False
    index_label: Optional[Union[str, bool]] = False
    quote_char: str = '"'
    line_terminator: str = os.linesep
    date_format: Optional[str] = None
    double_quote: bool = True
    escape_char: Optional[str] = None
    decimal: str = "."
    filename_ext: str = hankai.lib.MimeTypeText.CSV.ext
    phone_region: str = "US"
    phone_format: Optional[PhoneNumberFormat] = PhoneNumberFormat.NATIONAL
    client_map_file: Optional[str] = None


class TransformFacesheetMaps:  # pylint: disable=too-many-instance-attributes
    """CSV maps."""

    def __init__(self) -> None:
        self.group_by: List[str] = ["OriginDocumentPage", "pid"]
        self.group_by_select: List[str] = [
            "OriginDocumentPage",
            "pid",
            "dotmap",
            "text_ocr",
            "confidence",
        ]
        self.parse_names: Tuple[str, ...] = (
            "AdmittingProviderName",
            "GuarantorName",
            "InsuredName",
            "PatientName",
            "SurgeonName",
        )
        self.parse_addresses: Tuple[str, ...] = (
            "GuarantorAddress",
            "InsuranceAddress",
            "PatientAddress",
        )
        self.syn_names: Dict[str, str] = {
            "Title": "title",
            "First": "first",
            "Middle": "middle",
            "Last": "last",
            "Suffix": "suffix",
            "Nickname": "nickname",
        }
        self.syn_phones: Dict[str, None] = {
            "Mobile": None,
            "Home": None,
            "Work": None,
        }
        self.syn_addresses: Dict[str, str] = {
            "1": "address1",
            "2": "address2",
            "City": "city",
            "State": "state",
            "ZipCode": "zip_code",
        }
        self.usaddress_tag_mapping = {
            "Recipient": "recipient",
            "AddressNumber": "address1",
            "AddressNumberPrefix": "address1",
            "AddressNumberSuffix": "address1",
            "StreetName": "address1",
            "StreetNamePreDirectional": "address1",
            "StreetNamePreModifier": "address1",
            "StreetNamePreType": "address1",
            "StreetNamePostDirectional": "address1",
            "StreetNamePostModifier": "address1",
            "StreetNamePostType": "address1",
            "CornerOf": "address1",
            "IntersectionSeparator": "address1",
            "LandmarkName": "address1",
            "USPSBoxGroupID": "address1",
            "USPSBoxGroupType": "address1",
            "USPSBoxID": "address1",
            "USPSBoxType": "address1",
            "BuildingName": "address2",
            "OccupancyType": "address2",
            "OccupancyIdentifier": "address2",
            "SubaddressIdentifier": "address2",
            "SubaddressType": "address2",
            "PlaceName": "city",
            "StateName": "state",
            "ZipCode": "zip_code",
        }
        self.syn_date_processed = "DateProcessed"


@dataclass
class TransformFacesheetClientMap:
    """Client JSON map elements for DocuVision API Transform Facesheet."""

    column: str
    maps: Optional[List[str]] = None
    na: Optional[str] = None  # pylint: disable=invalid-name


class DotmapValueCI:
    """Implementation for collection of dotmap to value and confidence."""

    def __init__(
        self,
        na_representation: str,
    ) -> None:
        self._dotmap_value_ci: Dict[str, Dict[str, float]] = {}
        self.na_representation = na_representation

    def add(  # pylint: disable=too-many-arguments
        self,
        dotmap: str,
        value: str,
        confidence: float,
        append: bool = False,
    ) -> None:
        """Add dotmap, value and confidence. Set append=True to append the
        dotmap value to the previous value and calculate a combined confidence.
        """
        valid_confidence = hankai.orchestrator.ConfidenceInterval.normalize(
            confidence=confidence
        )

        if dotmap not in self._dotmap_value_ci:
            self._dotmap_value_ci[dotmap] = {value: valid_confidence}
        elif append:
            self._dotmap_value_ci[dotmap][value] = valid_confidence
        else:
            prev_ci = self.confidence(dotmap=dotmap)
            prev_value = list(self._dotmap_value_ci[dotmap].keys())
            if (
                len(prev_value) == 1
                and prev_value[0] == self.na_representation
                and value != self.na_representation
            ) or (valid_confidence >= prev_ci):
                self._dotmap_value_ci[dotmap] = {value: valid_confidence}

    def present(self, dotmap: str) -> bool:
        """Return True if dotmap present and False otherwise."""
        return dotmap in self._dotmap_value_ci

    def dotmaps(self) -> List[str]:
        """Return the dotmaps."""
        return list(self._dotmap_value_ci.keys())

    def values(self, dotmap: str) -> List[str]:
        """Return the dotmap values."""
        if not self.present(dotmap=dotmap):
            return []

        value_cis = self._dotmap_value_ci[dotmap]
        return list(value_cis.keys())

    def dotmaps_values(self) -> Dict[str, List[str]]:
        """Return all dotmaps and corresponding values."""
        dotmap_value: Dict[str, List[str]] = {}
        for dotmap in self._dotmap_value_ci:
            dotmap_value[dotmap] = self.values(dotmap=dotmap)

        return dotmap_value

    def value(self, dotmap: str, na_representation: str, join: str = " ") -> str:
        """Return the dotmap values concatenated."""
        if not self.present(dotmap=dotmap):
            return na_representation

        return join.join(self.values(dotmap=dotmap))

    def confidence(self, dotmap: str) -> float:
        """Return the dotmap confidence."""
        if not self.present(dotmap=dotmap):
            return hankai.orchestrator.ConfidenceInterval.MIN.value

        value_cis = self._dotmap_value_ci[dotmap]
        values = value_cis.values()
        try:
            return sum(values) / len(values)
        except Exception:  # pylint: disable=broad-except
            pass

        return hankai.orchestrator.ConfidenceInterval.MIN.value

    def delete(self, dotmap: str) -> None:
        """Delete the dotmap entry."""
        if self.present(dotmap=dotmap):
            del self._dotmap_value_ci[dotmap]
