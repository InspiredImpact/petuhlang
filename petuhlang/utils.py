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
"""Library utilities."""

from __future__ import annotations

import io
import os
import sys
import typing

if typing.TYPE_CHECKING:
    from types import TracebackType

    ExcType = typing.Type[BaseException]


__all__: tuple[str, ...] = (
    "get_memory_location",
    "on_windows",
    "is_builtin",
    "get_current_filename",
    "OutputInterceptor",
)


def get_memory_location(obj: typing.Any, /) -> str:
    """``utility function``

    Nice output of object id:)

    obj: :class:`typing.Any`
        Object to display "memory location".
    """
    return hex(id(obj))


def on_windows() -> bool:
    """``utility function``

    Checking the current operating system.
    """
    return os.name == "nt"


def is_builtin(name: str, /) -> bool:
    """``utility function``

    Checks if a name is a dunder or a petuhlang-builtin object.

    name: :class:`str` [Positional-only]
        Name to check.
    """
    return name.startswith("__") or name in {
        "__filter__",
        "__pbuiltins__",
        "__pobject__",
    }


def get_current_filename() -> str:
    """``utility function``

    Get the name of the current file in which the code is called.
    """
    _split_by = " \ ".strip()
    return __file__.split(_split_by)[-1]


class OutputInterceptor(list):
    """Context manager-interceptor of console output."""

    def __enter__(self) -> OutputInterceptor:
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self

    def __exit__(
        self,
        exc_type: ExcType | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout
