from pytest import mark
from automated_tests.api_util import send_request


@mark.smoke
def test__smoke__api__verify_versions(empty_database_fixture_function):
    expected_values = {"api_version": "0_1", "app_version": "0_5_1"}
    for endpoint in ["v1", "v1/status"]:
        request_response = send_request(endpoint)
        assert request_response.status_code == 200, f"Expected: 200, actual: {request_response.status_code}"
        for key in expected_values:
            expected_value = expected_values[key]
            actual_value = request_response.json()[key]
            assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.smoke
def test__smoke__api__verify_statuses(empty_database_fixture_function):
    expected_values = {"api_status": 200, "app_status": 200, "db_status": 200}
    for endpoint in ["v1", "v1/status"]:
        request_response = send_request(endpoint)
        assert request_response.status_code == 200, f"Expected: 200, actual: {request_response.status_code}"
        for key in expected_values:
            expected_value = expected_values[key]
            actual_value = request_response.json()[key]
            assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
