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
"""All petuhlang errors."""

import typing

import petuhlang.cli.colors.impl as cli  # circular
from petuhlang.types import ClsDecoratorT


__all__: tuple[str, ...] = (
    # Global errors.
    "PetuhError",
    "ObjectIsImmutableError",
    "ObjectIsNotCallableError",
    # Enums errors.
    "InappropriateTypeSpecifiedError",
    # Ext errors.
    "EXTError",
    # String errors.
    "StringError",
    "CharIsTooLongError",
    # Function errors.
    "FunctionError",
    "BadFunctionArgError",
    # Class errors.
    "ClassError",
    "BadParentClassPassedError",
)


_DEFAULT_TEMPLATE: typing.Final[
    str
] = "An error was thrown for the following reason -> "


def _with_error_manipulator(*, template: str = _DEFAULT_TEMPLATE) -> ClsDecoratorT:
    """``decorator``

    Changes the style and color of the error output to the console.

    template: :class:`str` = _DEFAULT_TEMPLATE
        Default error template.
    """

    def inner(cls: type) -> type:
        cls.__str__ = lambda self: (
            cli.cprint(
                f"\n"
                # Skipping to new line.
                f"{template}",
                # Using template in at the beginning of the error message.
                color="LIGHT_WHITE",
                return_str=True,
            )
            # Making the beginning of the error message of a different color.
            + f"{self.args[0]}\n"
            # An error message is always expected as the first argument
            # (at the convention level, there may be exceptions).
            + (" " * len(template))
            # Multiply by the length of the template to highlight the error text.
            + ("^" * len(self.args[0]))
            # Creating arrows to highlight the error.
        )
        return cls

    return inner


@_with_error_manipulator()
class PetuhError(Exception):
    """Base petuhlang error."""


# global errors
class ObjectIsNotCallableError(PetuhError):
    """Raised when trying to invoke a non-callable object."""


class ObjectIsImmutableError(PetuhError):
    """Raised when trying to modify an immutable object."""


# base.enums
class InappropriateTypeSpecifiedError(PetuhError):
    """Raised when the enumeration type does not match @only(type)."""


# __future__ext
class EXTError(PetuhError):
    """Base ext error."""


# __future__ext.strings
class StringError(EXTError):
    """Base string error."""


class CharIsTooLongError(StringError):
    """Raised when the length of the character for centering is more than 1."""


# functions
class FunctionError(PetuhError):
    """Base function error."""


class BadFunctionArgError(FunctionError):
    """Raised when bad function argument passed."""


# classes
class ClassError(PetuhError):
    """Base class error."""


class BadParentClassPassedError(ClassError):
    """Raised when bad parent class passed."""
