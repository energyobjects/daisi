import pydaisi as pyd

def test_hello_world():
    with pyd.Daisi("wkoteras/hello_world") as my_daisi:
        output = my_daisi.hello_world().value
        assert output == "Hello World"
