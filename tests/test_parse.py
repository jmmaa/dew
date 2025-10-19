def test_readme_example():
    import dew

    result = dew.parse("add rgb color r=100 g= 150 b=200")

    args = result["args"]

    kwargs = result["kwargs"]

    assert args[0] == "add"
    assert args[1] == "rgb"
    assert args[2] == "color"

    assert kwargs[0][0] == "r" and kwargs[0][1] == "100"
    assert kwargs[1][0] == "g" and kwargs[1][1] == "150"
    assert kwargs[2][0] == "b" and kwargs[2][1] == "200"


def test_dash_prefix():
    import dew

    result = dew.parse("addr -aggro")

    args = result["args"]

    kwargs = result["kwargs"]

    assert args[0] == "addr"
    assert args[1] == "-aggro"

    assert len(kwargs) == 0


def test_escape_chars():
    import dew

    result = dew.parse("addr -\\=aggro")

    args = result["args"]

    kwargs = result["kwargs"]

    assert args[0] == "addr"
    assert args[1] == "-=aggro"

    assert len(kwargs) == 0

    result = dew.parse("addr -\\=aggro gg\\\\\\=wp")

    args = result["args"]

    kwargs = result["kwargs"]

    assert args[0] == "addr"
    assert args[1] == "-=aggro"
    assert args[2] == "gg\\=wp"
    assert len(kwargs) == 0


def test_newlines():
    import dew

    result = dew.parse("""
    
    add rgb color 
    r=100 
    g=150 
    b=200


    """)

    args = result["args"]

    kwargs = result["kwargs"]

    assert args[0] == "add"
    assert args[1] == "rgb"
    assert args[2] == "color"

    assert kwargs[0][0] == "r" and kwargs[0][1] == "100"
    assert kwargs[1][0] == "g" and kwargs[1][1] == "150"
    assert kwargs[2][0] == "b" and kwargs[2][1] == "200"
