import pytest
import pydaisi as pyd

@pytest.mark.parametrize("name, expected_output", [("Daisi user", "Hello Daisi user, from the Daisi platform"), 
                                                   ("blah", "Hello blah, from the Daisi platform")])
def test_hello(name, expected_output):
    greeting_daisi = pyd.Daisi("exampledaisies/Print Hello")
    output = greeting_daisi.hello(name = name).value
    assert output == expected_output

