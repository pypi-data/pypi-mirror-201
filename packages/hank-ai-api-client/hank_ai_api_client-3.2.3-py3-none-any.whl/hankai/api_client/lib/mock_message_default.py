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
"""DocuVision Mock Message defaults."""

import random
from dataclasses import dataclass

import hankai.aws
import hankai.lib
import hankai.orchestrator


@dataclass
class MockDefault:  # pylint: disable=too-many-instance-attributes
    """MockMessage defaults."""

    encoding: hankai.lib.Encoding = hankai.lib.Encoding(
        base=hankai.lib.EncodeBinaryBase.BASE_64,
        codec=hankai.lib.EncodeStringCodec.UTF_8,
    )
    mime_type: hankai.lib.MimeType = hankai.lib.MimeType(
        mime_type=hankai.lib.MimeTypeApplication.PDF
    )
    confidence_interval: float = 0.85
    perform_ocr: bool = True
    response_state: hankai.orchestrator.ResponseState = random.choice(
        [
            hankai.orchestrator.ResponseState.IN_PROGRESS,
            hankai.orchestrator.ResponseState.COMPLETED,
            hankai.orchestrator.ResponseState.ERROR,
        ]
    )
    redact: bool = True
    picklable: bool = False
