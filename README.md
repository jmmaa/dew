
## Dew<br>![PyPI](https://img.shields.io/pypi/v/dew-py?label=version)


A simple command language inspired from discord slash commands

```py
import pprint as pp

import dew


result = dew.parse('add rgb color name:"my color" r:100 g:150 b:200')


pp.pprint(result)

# {'name': 'add',
#  'tail': {'name': 'rgb',
#           'tail': {'name': 'color',
#                    'tail': [('name', 'my color'),
#                             ('r', '100'),
#                             ('g', '150'),
#                             ('b', '200')]}}}
```

### Links

[BNF grammar](grammar.bnf)
