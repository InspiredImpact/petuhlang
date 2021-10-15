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

from __future__ import annotations

import typing

from petuhlang import PetuhObject, with_convert
from petuhlang.__future__ext.strings.containers import Center
from petuhlang.__future__converters.abstract import ConverterABC

if typing.TYPE_CHECKING:
    T = typing.TypeVar("T")
    ContainerOr = typing.Union[T, Center]

    from petuhlang.types.maybe import MaybeNone


class _StringConverter(ConverterABC):
    """
    !!! note:
        This is a Future object that will be relevant in
        future versions of petuhlang. There is no point
        in using it right now.
    """

    def convert(self, argument: typing.Any) -> typing.Any:
        return self.__received_cls__(argument)


@with_convert(converter=_StringConverter())
class PaddingString(PetuhObject):
    """
    !!! note:
        This is a Future object that will be relevant in
        future versions of petuhlang. There is no point
        in using it right now.
    """

    def __init__(
        self, string_: str, /, *, center: MaybeNone[ContainerOr[tuple[int, str]]] = None
    ) -> None:
        self.__string = string_
        self.__center = center

        if not isinstance(self.__center, Center):
            self.__center = Center.from_tuple(self.__center)

    def __call__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        if not self.__center:
            return self.__string
        else:
            return self.__string.center(self.__center.width, self.__center.fill_char)
