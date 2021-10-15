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
"""Keywords in petuhlang."""

from __future__ import annotations

import typing

from petuhlang import PetuhObject
from .utils import OutputInterceptor


__all__: tuple[str, ...] = ("then", "function", "pyclass", "retrieve")


class _KeywordBase(PetuhObject):
    """Base for all keyword classes"""

    def __rshift__(self, other: typing.Any) -> _KeywordBase:
        """Overload >> operator."""
        return self


class _Then(PetuhObject):
    """'then' keyword"""

    def __getitem__(self, smth: typing.Any) -> _Then:
        """Overload [] operator for 'then' keyword."""
        with OutputInterceptor() as output:
            ret = smth() if callable(smth) else smth

        self.__to_compile__ = ret

        for text in output:
            __builtins__.print(text)

        return self


class _Function(_KeywordBase):
    """'function' keyword."""


class _PyClass(_KeywordBase):
    """'pyclass' keyword."""


class _Retrieve(PetuhObject):
    """'retrieve' keyword (like return in python)."""

    def __rshift__(self, other: typing.Any) -> typing.Any:
        """Overload >> operator."""
        return other


then = _Then()
function = _Function()
pyclass = _PyClass()
retrieve = _Retrieve()
