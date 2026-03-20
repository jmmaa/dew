
## Dew

A mini command language.

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

This command language works similarly to python's function argument behavior. Positional Arguments comes first before Keyword Arguments. The keyword arguments are defined by using '=' operator while positional arguments wont need any.

```
rgb                             ✔
rgb color                       ✔
rgb color r=100 g=100 b=100     ✔
r=100 rgb                       ✘
```

Positional Arguments and Keyword Arguments (both key and value) can be defined in 3 possible ways and will be evaluated all the same manner, however quotes `'` and double quotes `"` allow you to add whitespaces on arguments
```
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