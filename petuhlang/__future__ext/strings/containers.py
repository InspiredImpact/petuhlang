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

import dataclasses

from petuhlang.errors import CharIsTooLongError


__all__: tuple[str, ...] = ("Center",)


@dataclasses.dataclass()
class Center:
    """
    !!! note:
        This is a Future object that will be relevant in
        future versions of petuhlang. There is no point
        in using it right now.
    """

    width: int
    fill_char: str = None

    def __len__(self) -> int:
        return self.width

    def __post_init__(self) -> None:
        if len(self.fill_char) > 1:
            raise CharIsTooLongError(
                "The length of the centering symbol cannot be more than 1"
            )

    @classmethod
    def from_tuple(cls, tuple_: tuple[int, str], /) -> Center:
        return cls(tuple_[0], tuple_[1])
