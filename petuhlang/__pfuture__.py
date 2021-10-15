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
"""Petuhlang futures which will be added in future versions of the library."""

from __future__ import annotations

import typing
import dataclasses

from petuhlang.types import ReleaseStage


VersionTuple = tuple[int, int, int, ReleaseStage]


__all__: tuple[str, ...] = (
    "FunctionInnerArgument",
    "FunctionArgumentConverter",
)


@dataclasses.dataclass(kw_only=True)
class _Version:
    """Future version object."""

    major: int
    minor: int
    micro: int
    release_stage: ReleaseStage

    def astuple(self) -> VersionTuple:
        """Returns future version object as tuple."""
        return typing.cast(VersionTuple, tuple(_ for _ in self.__dict__.values()))


@dataclasses.dataclass(kw_only=True)
class _Future:
    """petuhlang future object."""

    available_from: _Version
    final_release_in: _Version

    def __str__(self) -> str:
        return "<Petuh.Future>"


FunctionInnerArgument = _Future(
    available_from=_Version(major=1, minor=5, micro=0, release_stage="alpha"),
    final_release_in=_Version(major=2, minor=0, micro=0, release_stage="alpha"),
)

FunctionArgumentConverter = _Future(
    available_from=_Version(major=1, minor=5, micro=0, release_stage="alpha"),
    final_release_in=_Version(major=2, minor=0, micro=0, release_stage="alpha"),
)
