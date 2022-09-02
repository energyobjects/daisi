import pydaisi as pyd

def test_hello_world():
    with pyd.Daisi("wkoteras/invert_image") as my_daisi:
        output = my_daisi.invert().value
        assert output == "Hello World"
