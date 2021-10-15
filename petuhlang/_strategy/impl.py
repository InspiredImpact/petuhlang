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
"""Strategy implementation."""

from __future__ import annotations

import typing

from .enums import CategoryEnum
from .abstract import StrategyABC
from petuhlang._functions import PetuhFunction
from petuhlang._classes import PetuhClass

if typing.TYPE_CHECKING:
    CategoryType = typing.Literal["functions", "classes"] | CategoryEnum


__all__: tuple[str, ...] = ("Strategy",)


class Strategy:
    """The class that defines the strategy."""

    def __init__(self, category: CategoryType, /) -> None:
        self.__category = category

        self.__categories: dict[str, type] = {
            CategoryEnum.strategy_functions: Functions,
            CategoryEnum.strategy_classes: Classes,
        }

    def get_default(self, name: str, /) -> typing.Any:
        """Returns default value for certain strategy."""
        return self.__categories[self.__category](name).default


class Functions(StrategyABC):
    """Function strategy."""

    @property
    def default(self) -> typing.Any:
        return PetuhFunction(self._obj_name)


class Classes(StrategyABC):
    """Classes strategy."""

    @property
    def default(self) -> typing.Any:
        return PetuhClass(self._obj_name)
