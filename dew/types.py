# MIT License
#
# Copyright (c) 2025 jma
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

# ruff: noqa: W505

"""dew library enum classes."""

import typing_extensions as t


class PositionalArgument(t.NamedTuple):
    """Represents the positional arguments."""

    value: str

    def __repr__(self) -> str:  # noqa: D105
        return f'PositionalArgument("{self.value}")'


class KeywordArgument(t.NamedTuple):
    """Represents the keyword arguments."""

    name: str
    value: str

    def __repr__(self) -> str:  # noqa: D105
        return f'KeywordArgument("{self.name}", "{self.value}")'


class Argument(t.NamedTuple):
    """Represents the Arguments."""

    value: PositionalArgument | KeywordArgument

    def __repr__(self) -> str:  # noqa: D105
        return f"Argument({self.value})"
