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

from dataclasses import dataclass
from typing import List, Optional, Set, Type

import hankai.lib
import hankai.orchestrator

from .docuvision_transform_facesheet import TransformFacesheetCSV
from .docuvision_transform_facesheet_csv_argparse import (
    TransformFacesheetCSVArgparse,
    TransformFacesheetCSVEnv,
)


class ServiceTransform(hankai.lib.MemberValueLower):
    """Service transformers."""

    FACESHEET_CSV = "facesheet_csv"


@dataclass
class SQSServiceTransformer:
    """Class for service and transforms details."""

    service: hankai.orchestrator.Service
    transform: ServiceTransform
    api_response_transform: Type[hankai.orchestrator.APIResponseTransform]
    api_response_transform_argparse: Optional[Type[hankai.lib.ArgparseHandler]] = None
    env: Optional[Type[hankai.lib.EnvEnum]] = None


class SQSTransform:
    """Hank AI Service transformer classes. Service transformers.
    Tuple of transformer type, optional argparse class and EnvEnum.
    """

    # def __init__(self) -> None:
    _transformers: List[SQSServiceTransformer] = []
    _transformers.append(
        SQSServiceTransformer(
            service=hankai.orchestrator.Service.DOCUVISION_1,
            transform=ServiceTransform.FACESHEET_CSV,
            api_response_transform=TransformFacesheetCSV,
            api_response_transform_argparse=TransformFacesheetCSVArgparse,
            env=TransformFacesheetCSVEnv,
        )
    )

    @classmethod
    def unique_api_response_transform_argparsers(
        cls,
    ) -> Set[Type[hankai.lib.ArgparseHandler]]:
        """Return unique SQS API Response Transformers. Primarily for command
        line --help.
        """
        api_response_transform_argparsers: Set[Type[hankai.lib.ArgparseHandler]] = set()
        for trn in cls._transformers:
            argparser: Optional[
                Type[hankai.lib.ArgparseHandler]
            ] = trn.api_response_transform_argparse
            if argparser:
                api_response_transform_argparsers.add(argparser)

        return api_response_transform_argparsers

    @classmethod
    def services(cls) -> List[hankai.orchestrator.Service]:
        """Return Services which have transformers."""
        services: List[hankai.orchestrator.Service] = []
        for trn in cls._transformers:
            services.append(trn.service)

        return services

    @classmethod
    def transforms(cls, service: hankai.orchestrator.Service) -> List[ServiceTransform]:
        """Return Service transforms."""
        transforms: List[ServiceTransform] = []
        for trn in cls._transformers:
            if trn.service is service:
                transforms.append(trn.transform)

        return transforms

    @classmethod
    def transformer(
        cls,
        service: hankai.orchestrator.Service,
        transform: ServiceTransform,
    ) -> Optional[SQSServiceTransformer]:
        """Return SQSServiceTransformer."""

        for trn in cls._transformers:
            if trn.service is service and trn.transform is transform:
                return trn

        return None
