def test_readme_example():
    import dew

    result = dew.parse('add rgb color name:"my color" r:100 g:150 b:200')

    assert result["command_name"] == "add"
    assert result["sub_command_group_name"] == "rgb"
    assert result["sub_command_name"] == "color"

    kwargs = result["kwargs"]

    if kwargs is not None:
        assert kwargs[0][1] == "my color"
        assert kwargs[1][1] == "100"
        assert kwargs[2][1] == "150"
        assert kwargs[3][1] == "200"


def test_command_name_only():
    import dew

    result = dew.parse("add")

    assert result["command_name"] == "add"
    assert result["sub_command_group_name"] is None
    assert result["sub_command_name"] is None

    assert result["kwargs"] is None


def test_command_name_with_kwargs():
    import dew

    result = dew.parse("add num:3 num:4")

    assert result["command_name"] == "add"
    assert result["sub_command_group_name"] is None
    assert result["sub_command_name"] is None

    assert result["kwargs"] is not None

    kwargs = result["kwargs"]
    if kwargs is not None:
        assert kwargs[0][0] == "num"
        assert kwargs[1][0] == "num"
        assert kwargs[0][1] == "3"
        assert kwargs[1][1] == "4"
