from pytest import mark
from selenium.webdriver.common.by import By
from automated_tests.streamlit_ui_util import create_release, create_requirement


@mark.smoke
def test__smoke__streamlit_app__dashboard_nav(two_fully_set_up_projects, selenium_util):
    expected_values = [2, 3, 5, 2]
    test_project_shortname = "new_project"
    for index, value in enumerate(selenium_util.driver.find_elements(By.XPATH, "//*[@data-testid='stMetricValue']")):
        actual_value = eval(value.text)
        expected_value = expected_values[index]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", test_project_shortname)
    expected_values = [1, 2, 3, 2]
    for index, value in enumerate(selenium_util.driver.find_elements(By.XPATH, "//*[@data-testid='stMetricValue']")):
        actual_value = eval(value.text)
        expected_value = expected_values[index]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.smoke
def test__smoke__streamlit_app__dashboard_summaries_releases(two_fully_set_up_projects, selenium_util):
    expected_value = "There is 1 empty release."
    target_project = "new_project"
    create_release(selenium_util, "not_covered_released", "not_covered_released", target_project)
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", target_project)
    assert expected_value in selenium_util.driver.page_source, f"Expected value: {expected_value} not in page source."


@mark.smoke
def test__smoke__streamlit_app__dashboard_summaries_requirements(two_fully_set_up_projects, selenium_util):
    expected_value = "There is 1 requirement not covered with test cases."
    create_requirement(selenium_util, "not_covered_requirement", "not_covered_requirement", "new_project", "req-3")
    assert expected_value in selenium_util.driver.page_source, f"Expected value: {expected_value} not in page source."


@mark.smoke
def test__smoke__streamlit_app__dashboard_summaries_bugs(two_fully_set_up_projects, selenium_util):
    expected_value = "There are 2 active bugs"
    assert expected_value in selenium_util.driver.page_source, f"Expected value: {expected_value} not in page source."
