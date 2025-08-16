

def test_readme_example():

    import dew

    result = dew.parse('add rgb color name:"my color" r:100 g:150 b:200')

    assert result["command_name"] == "add"
    assert result["sub_command_group_name"] == "rgb"
    assert result["sub_command_name"] == "color"

    assert result["kwargs"][0][1] == "my color"
    assert result["kwargs"][1][1] == "100"
    assert result["kwargs"][2][1] == "150"
    assert result["kwargs"][3][1] == "200"
