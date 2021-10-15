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
"""Functions implementation in petuhlang."""

from __future__ import annotations

import sys
import types
import typing
import textwrap

from .arguments import Arg, Kwarg, FnArgBase
from petuhlang import errors, __pfuture__
from petuhlang.utils import get_memory_location, get_current_filename

if typing.TYPE_CHECKING:
    from petuhlang.types import ArgsType, KwargsType

    Arg: FnArgBase
    Kwarg: FnArgBase

    T = typing.TypeVar("T")
    StringOr = typing.Union[T, str]


__all__: tuple[str, ...] = ("PetuhFunction",)

global_ = sys.modules["builtins"].__dict__


def _build_function_args(args: typing.Sequence[Arg | Kwarg], /) -> str:
    args = (i.name for i in args if isinstance(i, Arg))
    kwargs = (f"{i.name}={i.value}" for i in args if isinstance(i, Kwarg))
    return ", ".join(args) if args else "" + ", " + ", ".join(kwargs) if kwargs else ""


def _build_function_code(*, name: str, args: str, fn_code: str) -> str:
    return f"def {name}({args}):\n{textwrap.indent(fn_code, '    ')}"


class _Callable:
    """Returning non-callable object as callable."""

    def __init__(self, value: typing.Any) -> None:
        self.__value = value

    def __call__(self, *args: ArgsType, **kwargs: KwargsType) -> typing.Any:
        return self.__value


class FunctionInner:
    """Compile function or returning value."""

    def __init__(self, fn_name: str, args: typing.Sequence[Arg | Kwarg]) -> None:
        self.__fn_name__ = fn_name
        self.__fn_args__ = args

    def __init_args(self, fn: types.FunctionType, /) -> types.FunctionType:
        for arg in self.__fn_args__:
            setattr(
                fn, arg.name, __pfuture__.FunctionInnerArgument
            )  # TODO: PRE-ALPHA-1.5.0, IMPL IN-2.0.0
        return fn

    def __compile_from_str(self, function_code: str) -> types.FunctionType:
        exec(
            _build_function_code(
                name=self.__fn_name__,
                args=_build_function_args(self.__fn_args__),
                fn_code=function_code,
            ),
            globals(),
            locals(),
        )
        fn = self.__init_args(eval(f"{self.__fn_name__}"))
        global_[self.__fn_name__] = fn
        return fn

    def __getitem__(self, function_code: StringOr[typing.Any]):
        if isinstance(function_code, str):
            return self.__compile_from_str(function_code)
        else:
            global_[self.__fn_name__] = (obj := _Callable(function_code))
            return obj


class PetuhFunction:
    """Preparing function."""

    def __init__(self, fn_name: str, /) -> None:
        self.__fn_name__ = fn_name

    def __call__(self, *function_args: ArgsType) -> FunctionInner:
        self.__function_arguments = function_args
        self.__check_call_args()
        return FunctionInner(self.__fn_name__, function_args)

    def __str__(self):
        return self.__fn_name__

    def __repr__(self):
        return f"<{self.__class__.__name__} object at {get_memory_location(self)}>"

    def __check_call_args(self) -> None:
        for arg in self.__function_arguments:
            if not isinstance(arg, (Arg, Kwarg)):
                raise errors.BadFunctionArgError(
                    f"All function arguments must be instances of the 'arg' or 'kwarg' class, got {type(arg)}"
                )
