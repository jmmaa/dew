# Dew

A simple parser for discord slash command-like text, written in pure python

```python
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
