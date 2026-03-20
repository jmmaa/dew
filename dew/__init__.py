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

"""A mini command language.

```py
import dew

args = dew.parse("add rgb color r=100 g= 150 b=200")

for arg in args:
    print(arg)

# Argument(PositionalArgument("add"))
# Argument(PositionalArgument("rgb"))
# Argument(PositionalArgument("color"))
# Argument(KeywordArgument("r", "100"))
# Argument(KeywordArgument("g", "150"))
# Argument(KeywordArgument("b", "200"))
```

### Install

```
pip install git+https://github.com/jmmaa/dew.git
```

### Links

[BNF grammar](grammar.bnf)


### Guide

This command language works similarly to python's function argument behavior. Positional
Arguments comes first before Keyword Arguments. The keyword arguments are defined by
using '=' operator while positional arguments wont need any.

```txt
rgb                             ✔
rgb color                       ✔
rgb color r=100 g=100 b=100     ✔
r=100 rgb                       ✘
```

Positional Arguments and Keyword Arguments (both key and value) can be defined in 3
possible ways and will be evaluated all the same manner, however quotes `'` and double
quotes `"` allow you to add whitespaces on arguments
```txt
# positional arguments
rgb
'rgb'
"rgb"

# keyword arguments
r=100
'r'='100'
"r"="100"

# with space

"simple argument"
'nice argument' = 100
"very nice argument" = 200
great_argument = 'this is a great argument'
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

__version__: t.Final[str] = "3.0.0.dev0"

__license__: t.Final[str] = "MIT"
