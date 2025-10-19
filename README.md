
## Dew


A simple command language inspired from python functions.

```py
import pprint as pp
import dew


result = dew.parse('add rgb color name="my color" r=100 g=150 b=200')

pp.pprint(result)

# {'args': ['add', 'rgb', 'color'],
# 'kwargs': [('name', 'my color'), ('r', '100'), ('g', '150'), ('b', '200')]}
```

### Install

```
pip install git+https://github.com/jmmaa/dew.git
```

### Links

[BNF grammar](grammar.bnf)
