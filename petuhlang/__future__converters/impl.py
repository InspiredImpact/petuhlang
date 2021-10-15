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
import contextlib

from petuhlang import __pfuture__
from .abstract import ConverterABC

if typing.TYPE_CHECKING:
    import collections.abc

    from petuhlang.types import MaybeNone

    ConverterT = typing.TypeVar("ConverterT", bound="BaseConverter")
    ConvertersType = dict[collections.abc.Hashable, typing.Type[ConverterT]]


__all__: tuple[str, ...] = ("BaseConverter",)


def _find_converter(type_: type, /) -> MaybeNone[ConverterT]:
    """
    !!! note:
        This is a Future object that will be relevant in
        future versions of petuhlang. There is no point
        in using it right now.
    """
    for types in __converters__.keys():
        if type_ in types or type_ is types:
            return __converters__[types]


class BaseConverter(ConverterABC):
    """
    !!! note:
        This is a Future object that will be relevant in
        future versions of petuhlang. There is no point
        in using it right now.
    """

    def __init__(self, *, type: type) -> None:
        self.__type = type

    def convert(self, argument: typing.Any) -> typing.Any:
        if isinstance(argument, self.__type):
            return argument
        with contextlib.suppress(Exception):
            return self.__type(argument)


BaseConverter = (
    __pfuture__.FunctionArgumentConverter
)  # TODO: PRE-ALPHA-1.5.0, IMPL IN-2.0.0


__converters__: ConvertersType = {(str, int, bool, dict, list): BaseConverter}
