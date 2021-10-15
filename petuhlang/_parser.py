# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021 DenyS
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
"""Parsing any names from python file by regex."""

import re
import sys

from ._dataclasses import ParsedFileContainer


__all__: tuple[str, ...] = ("parse_current_file",)


function_pattern: re.Pattern[str] = re.compile(
    r"""^function >> ([a-zA-Z]*\w+)""", re.MULTILINE
)
class_pattern: re.Pattern[str] = re.compile(
    r"""^pyclass >> ([a-zA-Z]*\w+)""", re.MULTILINE
)


def _extract_names_by(code: str, /, *, pattern: re.Pattern[str]) -> list[str]:
    """``function``

    Extracting any names from python file by regex.

    code: :class:`str` [Positional-only]
        Some python code.

    pattern: :class:`re.Pattern` [Keyword-only]
        The pattern by which the names will be extracted.
    """
    matches: list[str] = []
    for match in pattern.findall(code):
        matches.append(match)

    return matches


def parse_current_file() -> ParsedFileContainer:
    """Opening current file and returning object with parsed names."""
    with open(sys.argv[0], "r", encoding="utf-8") as file:
        code = file.read()

    return ParsedFileContainer(
        functions=_extract_names_by(code, pattern=function_pattern),
        classes=_extract_names_by(code, pattern=class_pattern),
    )
