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
"""Petuhlang enumerations."""

from __future__ import annotations

import typing

from petuhlang import errors
from petuhlang.utils import is_builtin

if typing.TYPE_CHECKING:
    from petuhlang.types.decos import ClsDecoratorT

    SelfT = typing.TypeVar("SelfT", bound="EnumBase")


__all__: tuple[str, ...] = (
    "Immutable",
    "Enum",
    "only",
)


def only(type_: type, /) -> ClsDecoratorT:
    """``enumeration decorator``

    Sets strictly 1 type for all enumerations, if something else is specified will cause an error.

    type_: :class:`type` [Positional-only]
        The type that will be checked against all other enumerations.
    """

    def inner(cls: type) -> type:
        for key, value in cls.__dict__.items():
            if not is_builtin(key) and not isinstance(value, type_):
                raise errors.InappropriateTypeSpecifiedError(
                    f"This type does not match the global enumeration type. "
                    f"(Expected {type_}, got {type(value)})"
                )
        return cls

    return inner


class Immutable:
    """Immutable class that is used to create immutable subclasses."""

    def __setitem__(self, _: typing.Any, __: typing.Any) -> typing.NoReturn:
        raise errors.ObjectIsImmutableError("Enums are immutable.")

    def __setattr__(self, _: typing.Any, __: typing.Any) -> typing.NoReturn:
        raise errors.ObjectIsImmutableError("Enums are immutable.")

    def __delattr__(self, _: typing.Any) -> typing.NoReturn:
        raise errors.ObjectIsImmutableError("Enums are immutable.")

    def __delitem__(self, _: typing.Any) -> typing.NoReturn:
        raise errors.ObjectIsImmutableError("Enums are immutable.")


class EnumBase(Immutable):
    """Base enum class."""

    def __getitem__(self: SelfT, item: str) -> typing.Any:
        return self.__members__[item]

    def __len__(self: SelfT) -> int:
        return len(self.__members__)

    def __repr__(self: SelfT) -> str:
        inner = ", ".join(f"{k}={v}" for k, v in self.__members__.items())
        return f"<Enum({inner})>"


class EnumMeta(type):
    """Enumeration metaclass."""

    def __new__(
        mcs: typing.Type[EnumMeta],
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, typing.Any],
    ) -> type:
        try:
            filter_ = attrs["__filter__"]
            if not callable(filter_):
                raise errors.ObjectIsNotCallableError("Callable object expected.")
        except KeyError:
            filter_ = lambda _: True

        members = {}
        for member in [m for m in attrs if not is_builtin(m) and filter_(m)]:
            members.update({member: attrs[member]})

        if bases:
            bases += (EnumBase,)

        attrs["__members__"] = members
        return super().__new__(mcs, name, bases, attrs)


class Enum(metaclass=EnumMeta):
    """Enumeration class."""

    if typing.TYPE_CHECKING:
        __members__: dict[str, typing.Any]

    def __iter__(self) -> typing.Iterator[str]:
        return iter(self.__members__.items())
