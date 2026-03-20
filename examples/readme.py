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
