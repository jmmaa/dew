def test_readme_example():
    import dew

    from dew.utils import get_kwargs

    result = dew.parse('add rgb color name:"my color" r:100 g:150 b:200')

    assert result["name"] == "add"

    # FIX THESE ERROR CASES
    tail = result["tail"]

    if isinstance(tail, dict):
        assert tail["name"] == "rgb"

        tail = tail["tail"]

        if isinstance(tail, dict):
            assert tail["name"] == "color"

    kwargs = get_kwargs(result)

    assert kwargs[0][1] == "my color"
    assert kwargs[1][1] == "100"
    assert kwargs[2][1] == "150"
    assert kwargs[3][1] == "200"


def test_dash_prefix():
    import dew

    from dew.utils import get_kwargs

    result = dew.parse("addr -aggro")

    if isinstance(result["tail"], dict):
        assert result["tail"]["name"] == "-aggro"
