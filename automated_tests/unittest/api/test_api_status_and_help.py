from json import loads
from re import findall
from pytest import mark
from src.api import get_help, get_help_by_request, status, return_response


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


@mark.unittest
def test__unittest__api__get_help():
    expected_keys = ["status", "get_help", "get_object", "get_objects", "insert_object"]
    actual_keys = loads(get_help())
    for expected_key in expected_keys:
        assert expected_key in actual_keys, f"{expected_key} not available in request response"


@mark.unittest
def test__unittest__api__get_help_by_request():
    expected_keys = ["description", "format"]
    for request_name in ["status", "get_help", "get_object", "get_objects", "insert_object"]:
        actual_keys = loads(get_help_by_request(request_name))
        for expected_key in expected_keys:
            assert expected_key in actual_keys, f"Missing {expected_key} field in {request_name}"
        if request_name != "status":
            additional_parameters = findall("<(.*?)>", actual_keys["format"])
            for group in additional_parameters:
                assert f"{group}_value" in actual_keys, f"Missing {group}_value field in {request_name}"
