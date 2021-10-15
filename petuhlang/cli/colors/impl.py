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
"""Colored output in console:)."""

from __future__ import annotations

import typing

from .enums import (
    AnsiBase,
    color as color_,
    background as background_,
    effect as effect_,
)
from petuhlang.utils import on_windows

if typing.TYPE_CHECKING:
    from petuhlang.types.maybe import MaybeNone

    _AllowedColorsType = typing.Literal[
        "BLACK",
        "RED",
        "GREEN",
        "YELLOW",
        "BLUE",
        "PURPLE",
        "CYAN",
        "WHITE",
        # Not part of the standard.
        "LIGHT_BLACK",
        "LIGHT_RED",
        "LIGHT_GREEN",
        "LIGHT_YELLOW",
        "LIGHT_BLUE",
        "LIGHT_MAGENTA",
        "LIGHT_CYAN",
        "LIGHT_WHITE",
    ]
    _EffectType = typing.Literal["BOLD", "ITALIC", "UNDERLINE", "REVERSE"]

    effect_: AnsiBase
    background_: AnsiBase
    color_: AnsiBase


__all__: tuple[str, ...] = ("cprint",)


if on_windows():
    import ctypes

    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def cprint(
    message: str,
    /,
    color: _AllowedColorsType,
    *,
    return_str: bool = False,
    effect: MaybeNone[_EffectType] = None,
    background: MaybeNone[_AllowedColorsType] = None,
) -> MaybeNone[str]:
    to_print = effect_["RESET"] + color_[color]
    if background is not None:
        to_print += background_[background]

    if effect is not None:
        to_print += effect_[effect]

    final = to_print + message + effect_["RESET"]
    if return_str:
        return final

    print(final)
