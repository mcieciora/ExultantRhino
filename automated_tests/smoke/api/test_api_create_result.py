from pytest import mark
from automated_tests.api_util import send_data


@mark.smoke
def test__smoke__api__create_result(empty_database_fixture_function):
    test_data = {
        "title": "develop_1",
        "project_shortname": "ExultantRhino",
        "build_url": "http://localhost:8080/job/MultibranchPipeline_ExultantRhino/job/develop/1",
        "passed": 0,
        "failed": 0,
        "skipped": 0
    }
    expected_value = {"shortname": "rst-0"}
    request_response = send_data(test_data)
    assert request_response.status_code == 200, f"Expected: 200, actual: {request_response.status_code}"
    actual_value = request_response.json()
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.smoke
def test__smoke__api__create_result_not_dict(empty_database_fixture_function):
    test_data = True
    expected_value = {"error": "Invalid JSON data."}
    request_response = send_data(test_data)
    assert request_response.status_code == 400, f"Expected: 400, actual: {request_response.status_code}"
    actual_value = request_response.json()
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
