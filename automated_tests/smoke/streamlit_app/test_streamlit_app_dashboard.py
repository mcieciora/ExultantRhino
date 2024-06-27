from pytest import mark
from selenium.webdriver.common.by import By


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
