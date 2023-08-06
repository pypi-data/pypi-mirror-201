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

import re
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

# https://github.com/derek73/python-nameparser
import nameparser  # type: ignore[import]

# https://github.com/daviddrysdale/python-phonenumbers
import phonenumbers

# https://usaddress.readthedocs.io/en/latest/
import usaddress  # type: ignore[import]

import hankai.lib
import hankai.orchestrator

from .docuvision_transform_facesheet_csv_default import (
    DotmapValueCI,
    TransformFacesheetMaps,
)
from .enum_other import PhoneNumberFormat


class CandidatePosition(Enum):
    """Address candidate positions."""

    SINGLE = 0
    PRIOR = 1
    COMBINED = 2


class TransformFacesheetCSVParser:  # pylint: disable=too-many-instance-attributes
    """Collection of parsers for different types and categories of data."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        dotmap_value_ci: DotmapValueCI,
        page_num: Any,
        pid: Any,
        dotmap: str,
        value: str,
        confidence: float,
        na_representation: str,
        phone_region: str,
        phone_format: Optional[PhoneNumberFormat],
        logenv: hankai.lib.LogEnv,
    ) -> None:
        self.dotmap_value_ci = dotmap_value_ci
        self.page_num = page_num
        self.pid = pid
        self.dotmap = dotmap
        self.value = value
        self.confidence = confidence
        self.na_representation = na_representation
        self.logenv = logenv
        self.phone_region = phone_region
        self.phone_format = phone_format
        self._usaddress_tag_weight_max = 4.5
        self._usaddress_tag_weight_drop_factor = 0.044422222  # 0.1999 / 4.5
        self.csv_maps = TransformFacesheetMaps()

    def _usaddress_tags(self, address: str) -> Tuple[Dict[str, str], str]:
        """Return the usaddres.tag tags and type."""
        tags: Tuple[Dict[str, str], str] = ({}, "")
        try:
            tags = usaddress.tag(
                address,
                tag_mapping=self.csv_maps.usaddress_tag_mapping,
            )
        except Exception:  # pylint: disable=broad-except
            if self.logenv.verbosity > 1:
                self.logenv.logger.warning(
                    "Exception for OriginDocumentPage [{}] PID [{}] "
                    "dotmap [{}] usaddress [{}] caught:\n{}",
                    self.page_num,
                    self.pid,
                    self.dotmap,
                    address,
                    hankai.lib.Util.formatted_traceback_exceptions(),
                )

        return tags

    def _usaddress_tag_weight(self, tags: Dict[str, str]) -> Tuple[float, float]:
        """Return the weight and confidence factor of US address tags.
        [address2] tag is weighted less.
        """
        weight: float = 0.0
        for tag in self.csv_maps.syn_addresses.values():
            if tags.get(tag):
                if tag == "address2":
                    weight += 0.25
                else:
                    weight += 1.0

        ci_factor = (
            self._usaddress_tag_weight_max - weight
        ) * self._usaddress_tag_weight_drop_factor

        return (weight, ci_factor)

    def _usaddress_prefer(  # pylint: disable=too-many-locals
        self, candidates: List[Tuple[str, float, CandidatePosition]]
    ) -> Tuple[str, float, Dict[str, str]]:
        """Determine which candidate has the better probability of being
        a more likely accurate US address and return the value and condfidence.
        """
        # List[(weight_float, ci_float, address, usaddress_tags)]
        candidates_by_weight: List[Tuple[float, float, str, Dict[str, str]]] = []
        # List[(weight_float, ci_float, address, usaddress_tags)]
        candidates_by_weight_ci: List[Tuple[float, float, str, Dict[str, str]]] = []

        # First get the weights.
        single_pos_ci_weight: float = hankai.orchestrator.ConfidenceInterval.MIN.value
        prior_pos_ci_weight: float = hankai.orchestrator.ConfidenceInterval.MIN.value
        confidence: float = hankai.orchestrator.ConfidenceInterval.MIN.value
        for candidate, confidence, position in candidates:
            tags = self._usaddress_tags(candidate)[0]
            weight, ci_factor = self._usaddress_tag_weight(tags=tags)
            # Adjust confidence up or down if weights changed by position.
            if position is CandidatePosition.SINGLE:
                single_pos_ci_weight = weight
                confidence -= ci_factor
            if position is CandidatePosition.PRIOR and weight >= single_pos_ci_weight:
                confidence += ci_factor
            elif (
                position is CandidatePosition.COMBINED and weight >= prior_pos_ci_weight
            ):
                confidence += ci_factor
            elif position is CandidatePosition.COMBINED:
                confidence -= ci_factor

            confidence = hankai.orchestrator.ConfidenceInterval.normalize(
                confidence=confidence
            )

            candidates_by_weight.append((weight, confidence, candidate, tags))

        # Remove candidates with same weight but lower confidence. Sort weight
        # high to low.
        sorted_candidates_by_weight = sorted(
            candidates_by_weight, key=lambda tup: tup[0], reverse=True
        )
        # Tuple(weight_float, ci_float, address)
        prev_can: Tuple[
            float, float, str, Dict[str, str]
        ] = sorted_candidates_by_weight[0]
        candidates_by_weight_ci.append(prev_can)

        for weight, confidence, candidate, tags in sorted_candidates_by_weight[1:]:
            prev_weight = prev_can[0]
            prev_ci = prev_can[1]

            if weight == prev_weight and confidence >= prev_ci:
                candidates_by_weight_ci.append((weight, confidence, candidate, tags))

        ret_ci = candidates_by_weight_ci[0][1]
        ret_addr = candidates_by_weight_ci[0][2]
        ret_tags = candidates_by_weight_ci[0][3]

        del candidates_by_weight
        del candidates_by_weight_ci
        del sorted_candidates_by_weight

        return (ret_addr, ret_ci, ret_tags)

    def _usaddress_syn_dotmaps(self, tags: Dict[str, str], confidence: float) -> None:
        """Set the synthesis dotmaps value and confidence."""
        for label, key in self.csv_maps.syn_addresses.items():
            syn_dotmap = self.dotmap + label
            tag = tags.get(key)
            prior_syn_present = self.dotmap_value_ci.present(dotmap=syn_dotmap)
            if not prior_syn_present:
                self.dotmap_value_ci.add(
                    dotmap=syn_dotmap,
                    value=tag if tag is not None else self.na_representation,
                    confidence=confidence
                    if tag is not None
                    else hankai.orchestrator.ConfidenceInterval.MIN.value,
                )
            else:
                prior_syn_ci = self.dotmap_value_ci.confidence(dotmap=syn_dotmap)
                prior_syn_val = self.dotmap_value_ci.value(
                    dotmap=syn_dotmap, na_representation=self.na_representation
                )
                if tag is not None:
                    if (
                        prior_syn_val is self.na_representation
                        or self.confidence >= prior_syn_ci
                    ):
                        self.dotmap_value_ci.add(
                            dotmap=syn_dotmap,
                            value=tag,
                            confidence=self.confidence,
                        )

    def address(self) -> bool:
        """Addresses."""
        if re.match(
            rf".*({'|'.join(self.csv_maps.parse_addresses)})({'|'.join(self.csv_maps.syn_addresses.keys())})$",  # pylint: disable=line-too-long
            self.dotmap,
        ):
            # Explicit *Address dotmaps. e.g. AddressCity
            self.dotmap_value_ci.add(
                dotmap=self.dotmap,
                value=self.value,
                confidence=self.confidence,
            )

            return True

        if re.match(rf".*({'|'.join(self.csv_maps.parse_addresses)})$", self.dotmap):
            candidates: List[Tuple[str, float, CandidatePosition]] = []
            candidates.append((self.value, self.confidence, CandidatePosition.SINGLE))

            if self.dotmap_value_ci.present(dotmap=self.dotmap):
                # Get prior.
                prior_addr_val = self.dotmap_value_ci.value(
                    dotmap=self.dotmap,
                    na_representation="",
                    join=", ",
                )
                prior_addr_ci = self.dotmap_value_ci.confidence(dotmap=self.dotmap)
                candidates.append(
                    (prior_addr_val, prior_addr_ci, CandidatePosition.PRIOR)
                )

                # Set prior and current.
                prior_and_cur_addr = prior_addr_val + ", " + self.value
                prior_and_cur_addr_ci = (prior_addr_ci + self.confidence) / 2.0
                candidates.append(
                    (
                        prior_and_cur_addr,
                        prior_and_cur_addr_ci,
                        CandidatePosition.COMBINED,
                    )
                )

            # Determine preferred address candidate.
            prefer_value, prefer_ci, prefer_tags = self._usaddress_prefer(
                candidates=candidates,
            )
            self.dotmap_value_ci.add(
                dotmap=self.dotmap,
                value=prefer_value,
                confidence=prefer_ci,
            )
            self._usaddress_syn_dotmaps(tags=prefer_tags, confidence=prefer_ci)

            return True

        return False

    def names(self) -> bool:
        """Names."""
        if re.match(
            rf".*({'|'.join(self.csv_maps.parse_names)})({'|'.join(self.csv_maps.syn_names.keys())})$",  # pylint: disable=line-too-long
            self.dotmap,
        ):
            # Explicit *Name dotmaps. e.g. PatientNameLast
            self.dotmap_value_ci.add(
                dotmap=self.dotmap,
                value=self.value,
                confidence=self.confidence,
            )

            return True

        if re.match(rf".*({'|'.join(self.csv_maps.parse_names)})$", self.dotmap):
            self.dotmap_value_ci.add(
                dotmap=self.dotmap,
                value=self.value,
                confidence=self.confidence,
            )

            try:
                humanname = nameparser.HumanName(self.value).as_dict()
                for label, key in self.csv_maps.syn_names.items():
                    name_val: Optional[str] = humanname[key]
                    syn_dotmap = self.dotmap + label
                    self.dotmap_value_ci.add(
                        dotmap=syn_dotmap,
                        value=name_val
                        if name_val is not None
                        else self.na_representation,
                        confidence=self.confidence,
                    )
            except Exception:  # pylint: disable=broad-except
                if self.logenv.verbosity > 1:
                    self.logenv.logger.warning(
                        "Exception for OriginDocumentPage [{}] PID [{}] "
                        "dotmap [{}] nameparser [{}] caught:\n{}",
                        self.page_num,
                        self.pid,
                        self.dotmap,
                        self.value,
                        hankai.lib.Util.formatted_traceback_exceptions(),
                    )

            return True

        return False

    def phones(self) -> bool:
        """Phones."""
        if re.match(
            rf".*Phone({'|'.join(self.csv_maps.syn_phones.keys())})$",
            self.dotmap,
        ):
            # Explicit *Phone dotmaps. e.g. PatientPhoneMobile
            self.dotmap_value_ci.add(
                dotmap=self.dotmap,
                value=self.value,
                confidence=self.confidence,
            )

            return True

        if re.match(r".*Phone$", self.dotmap):
            try:
                phone = phonenumbers.parse(self.value, self.phone_region)
                if (
                    phonenumbers.is_valid_number(phone)
                    and self.phone_format is not None
                ):
                    phone_formated = phonenumbers.format_number(
                        phone, self.phone_format.value
                    )
                    self.dotmap_value_ci.add(
                        dotmap=self.dotmap,
                        value=phone_formated,
                        confidence=self.confidence,
                    )
                else:
                    self.dotmap_value_ci.add(
                        dotmap=self.dotmap,
                        value=self.value,
                        confidence=self.confidence,
                    )
            except Exception:  # pylint: disable=broad-except
                if self.logenv.verbosity > 1:
                    self.logenv.logger.warning(
                        "Exception for OriginDocumentPage [{}] PID [{}] "
                        "dotmap [{}] phonenumbers [{}] caught:\n{}",
                        self.page_num,
                        self.pid,
                        self.dotmap,
                        self.value,
                        hankai.lib.Util.formatted_traceback_exceptions(),
                    )

            return True

        return False
