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
"""Building "body" of petuhlang."""

from __future__ import annotations

import sys
import typing
import dataclasses

from ._strategy import Strategy
from ._enums import PetuhLangEnum
from ._parser import parse_current_file
from ._functions import Arg, Kwarg
from .cli.console import console, _Console
from .pkeywords import (
    function,
    _Function,
    then,
    _Then,
    pyclass,
    _PyClass,
    retrieve,
    _Retrieve,
)


if typing.TYPE_CHECKING:
    BuiltinsType = dict[str, type]
    UsingType = typing.Literal["petuhlang"]


__all__: tuple[str, ...] = (
    "using",
    "__pbuiltins__",
)


global_ = sys.modules["builtins"].__dict__


class _Unprintable:
    """Makes object unprintable."""

    def __str__(self) -> typing.NoReturn:
        raise TypeError("Unprintable object.")


class _Using:
    """'using' keyword in petuhlang (init petuhlang)."""

    def __rshift__(self, lname: UsingType) -> _Unprintable:
        """Initializing petuhlang (unprintable)."""
        self.__check_using(lname)
        self.__setup_builtins()
        self.__add_missing_objects()
        return _Unprintable()

    def __setup_builtins(self):
        """Adding petuh-builtins to python builtins."""
        for bname, bvalue in __pbuiltins__.items():
            global_.update({bname: bvalue})

    def __check_using(self, lname: UsingType, /) -> None:
        """Checking for `using` name."""
        if lname.lower() != PetuhLangEnum.name:
            raise TypeError(f"{PetuhLangEnum.name} expected, got {lname}")

    def __add_missing_objects(self) -> None:
        """Adding petuh-functions and petuh-classes to python builtins."""
        parsed_objects = dataclasses.asdict(parse_current_file())
        for obj_category in parsed_objects:
            strategy = Strategy(obj_category)
            for item in parsed_objects[obj_category]:
                global_[item] = strategy.get_default(item)


@dataclasses.dataclass()
class Builtins:
    """petuhlang builtins."""

    function: _Function = dataclasses.field(default=function)
    pyclass: _PyClass = dataclasses.field(default=pyclass)
    arg: Arg = dataclasses.field(default=Arg)
    then: _Then = dataclasses.field(default=then)
    kwarg: Kwarg = dataclasses.field(default=Kwarg)
    console: _Console = dataclasses.field(default=console)
    retrieve: _Retrieve = dataclasses.field(default=retrieve)


using = _Using()

__pbuiltins__: BuiltinsType = dataclasses.asdict(Builtins())
