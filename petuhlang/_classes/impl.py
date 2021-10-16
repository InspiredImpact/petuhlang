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
"""Classes implementation in petuhlang."""

from __future__ import annotations

import sys
import typing

from petuhlang import PetuhObject, errors

if typing.TYPE_CHECKING:
    from petuhlang.types import ArgsType, KwargsType, MaybeNone

    ClsParents = typing.Sequence[type, ...] | type


__all__: tuple[str, ...] = ("PetuhClass",)

global_ = sys.modules["builtins"].__dict__


def _check_cls_parents(cls_name: str, /, *, parents: ClsParents) -> None:
    """Checking if the class or classes was passed."""
    if not isinstance(parents, type):
        if bad_args := "".join(
            f"{obj}({type(obj)}), " for obj in parents if not isinstance(obj, type)
        ):
            raise errors.BadParentClassPassedError(
                f"Excepted classes for {cls_name}, got {bad_args}"
            )


def _create_instance(cls, *args: ArgsType, bindTo: str, **kwargs: KwargsType):
    """Body for classmethod."""
    global_[bindTo] = (instance := cls(*args, **kwargs))
    return instance


def _concatenate_bases(other: tuple[type, ...] | type) -> tuple[type, ...]:
    """Concatenating tuples."""
    if isinstance(other, type):
        return PetuhObject, other
    return (PetuhObject,) + other


class PetuhClass(PetuhObject):
    def __init__(self, cls_name: str, /) -> None:
        self.__cls_name__ = cls_name

    def __call__(self, *, extends: MaybeNone[ClsParents] = None) -> type:
        if extends is not None:
            _check_cls_parents(self.__cls_name__, parents=extends)
            bases = _concatenate_bases(extends)
        else:
            bases = (PetuhObject,)

        cls = type(
            self.__cls_name__,
            bases,
            {
                "createInstance": classmethod(_create_instance),
                "__init__": lambda self_, *args, **kwargs: None,
            },
        )
        global_[self.__cls_name__] = cls

        return cls
