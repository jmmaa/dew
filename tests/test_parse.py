from dew.types import KeywordArgument


def test_readme_example():
    import dew

    args = dew.parse("add rgb color r=100 g= 150 b=200")

    arg = args.pop(0).value.value
    assert arg == "add"

    arg = args.pop(0).value.value
    assert arg == "rgb"

    arg = args.pop(0).value.value
    assert arg == "color"

    arg = args.pop(0).value
    assert isinstance(arg, KeywordArgument)
    assert arg.name == "r"
    assert arg.value == "100"

    arg = args.pop(0).value
    assert isinstance(arg, KeywordArgument)
    assert arg.name == "g"
    assert arg.value == "150"

    arg = args.pop(0).value
    assert isinstance(arg, KeywordArgument)
    assert arg.name == "b"
    assert arg.value == "200"


def test_dash_prefix():
    import dew

    args = dew.parse("addr -aggro")

    arg = args.pop(0).value.value
    assert arg == "addr"

    arg = args.pop(0).value.value
    assert arg == "-aggro"


def test_escape_chars():
    import dew

    args = dew.parse("addr -\\=aggro")

    arg = args.pop(0).value.value
    assert arg == "addr"

    arg = args.pop(0).value.value
    assert arg == "-=aggro"

    args = dew.parse("addr -\\=aggro gg\\\\\\=wp")

    arg = args.pop(0).value.value
    assert arg == "addr"

    arg = args.pop(0).value.value
    assert arg == "-=aggro"

    arg = args.pop(0).value.value
    assert arg == "gg\\=wp"


def test_newlines():
    import dew

    args = dew.parse("""
    
    add rgb color 
    r=100 
    g=150 
    b=200


    """)

    arg = args.pop(0).value.value
    assert arg == "add"

    arg = args.pop(0).value.value
    assert arg == "rgb"

    arg = args.pop(0).value.value
    assert arg == "color"

    arg = args.pop(0).value
    assert isinstance(arg, KeywordArgument)
    assert arg.name == "r"
    assert arg.value == "100"

    arg = args.pop(0).value
    assert isinstance(arg, KeywordArgument)
    assert arg.name == "g"
    assert arg.value == "150"

    arg = args.pop(0).value
    assert isinstance(arg, KeywordArgument)
    assert arg.name == "b"
    assert arg.value == "200"
