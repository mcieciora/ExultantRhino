from pytest import mark
from selenium.webdriver.common.by import By


@mark.smoke
def test__smoke__streamlit_app__dashboard_nav(one_object_of_type_database_fixture, selenium_util):
    expected_value = 0
    test_project_shortname = "new project"
    for value in selenium_util.driver.find_elements(By.XPATH, f"//*[@data-testid='stMetricValue']"):
        actual_value = eval(value.text)
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", test_project_shortname)
    expected_value = 1
    for value in selenium_util.driver.find_elements(By.XPATH, f"//*[@data-testid='stMetricValue']"):
        actual_value = eval(value.text)
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
