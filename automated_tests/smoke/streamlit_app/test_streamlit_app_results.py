from os import environ
from pytest import mark
from re import findall


@mark.smoke
def test__smoke__streamlit_app__verify_results(multiple_results, selenium_util):
    selenium_util.go_to_page(f"http://{environ['APX_HOST']}:8501/Results")
    expected_value = 5
    actual_value = len(findall(r"develop_\d+", selenium_util.driver.page_source))
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
    expected_value = 1
    for value in ["33.0%", "87.0%", "100.0%"]:
        actual_value = len(findall(fr"{value}", selenium_util.driver.page_source))
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
    expected_value = 3
    actual_value = len(findall("0.0%", selenium_util.driver.page_source))
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
