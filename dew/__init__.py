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

"""A simple command language inspired from python functions.

```py
import pprint as pp
import dew


result = dew.parse('add rgb color name="my color" r=100 g=150 b=200')

# {
#     "args": [
#         "add",
#         "rgb",
#         "color"
#     ],
#     "kwargs": [
#         ("name", "my color"),
#         ("r", "100"),
#         ("g", "150"),
#         ("b", "200")
#     ],
# }
```
"""

import typing as t

from dew.parser import Command, parse

__all__ = [
    "Command",
    "parse",
]

__author__: t.Final[str] = "jma"

__email__: t.Final[str] = "withketa@gmail.com"

__version__: t.Final[str] = "2.0.0.dev0"

__license__: t.Final[str] = "MIT"
