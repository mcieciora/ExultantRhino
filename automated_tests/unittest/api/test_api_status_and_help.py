from pytest import mark
from src.api import status, return_response


@mark.unittest
def test__unittest__api__return_response__list_input():
    input_data = [{"test_key_1": "test_value_1"}]
    expected_value = '[{"test_key_1": "test_value_1"}]'
    actual_value = return_response(input_data)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.unittest
def test__unittest__api__status():
    expected_value = '[{"app_status": 200, "api_status": 200, "db_status": 200}]'
    actual_value = status()
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
