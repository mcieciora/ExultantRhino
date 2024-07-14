from pytest import mark
from selenium.webdriver.common.by import By
from automated_tests.streamlit_ui_util import create_bug, create_release, create_requirement, create_test_case


@mark.smoke
def test__smoke__streamlit_app__dashboard_nav(two_fully_set_up_projects, selenium_util):
    expected_values = [2, 3, 5, 2]
    test_project_shortname = "new_project"
    for index, value in enumerate(selenium_util.driver.find_elements(By.XPATH, "//*[@data-testid='stMetricValue']")):
        actual_value = eval(value.text)
        expected_value = expected_values[index]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project_select_box", test_project_shortname)
    expected_values = [1, 2, 3, 2]
    for index, value in enumerate(selenium_util.driver.find_elements(By.XPATH, "//*[@data-testid='stMetricValue']")):
        actual_value = eval(value.text)
        expected_value = expected_values[index]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.smoke
def test__smoke__streamlit_app__dashboard_summaries_releases(empty_database_fixture_session, selenium_util):
    expected_value = "Notification. There is 1 empty release."
    create_release(selenium_util, "not_covered_release", "not_covered_release", "DEFAULT")
    selenium_util.click_link_text("Dashboard")
    assert expected_value in selenium_util.driver.page_source, f"Expected value: {expected_value} not in page source."
    expected_value = "Notification. There are 2 empty releases."
    create_release(selenium_util, "not_covered_release", "not_covered_release", "DEFAULT")
    selenium_util.click_link_text("Dashboard")
    assert expected_value in selenium_util.driver.page_source, f"Expected value: {expected_value} not in page source."


@mark.smoke
def test__smoke__streamlit_app__dashboard_summaries_requirements(empty_database_fixture_session, selenium_util):
    expected_values = ["Notification. There is 1 empty release.",
                       "Notification. There is 1 requirement not covered with test cases."]
    create_requirement(selenium_util, "not_covered_requirement", "not_covered_requirement", "DEFAULT", "rls-0")
    selenium_util.click_link_text("Dashboard")
    for expected_value in expected_values:
        assert expected_value in selenium_util.driver.page_source, f"Expected value: {expected_value} not in page " \
                                                                   f"source."
    expected_value = "Notification. There are 2 requirements not covered with test cases."
    create_requirement(selenium_util, "not_covered_requirement", "not_covered_requirement", "DEFAULT", "rls-1")
    selenium_util.click_link_text("Dashboard")
    assert expected_value in selenium_util.driver.page_source, f"Expected value: {expected_value} not in page source."


@mark.smoke
def test__smoke__streamlit_app__dashboard_summaries_bugs(empty_database_fixture_session, selenium_util):
    create_test_case(selenium_util, "test_test_case", "test_test_case", "DEFAULT", "req-0")
    selenium_util.click_link_text("Dashboard")
    expected_value = "Notification. There is 1 active bug."
    create_bug(selenium_util, "test_bug", "test_bug", "DEFAULT", "tc-0")
    selenium_util.click_link_text("Dashboard")
    assert expected_value in selenium_util.driver.page_source, f"Expected value: {expected_value} not in page source."
    expected_value = "Notification. There are 2 active bugs."
    create_bug(selenium_util, "test_bug", "test_bug", "DEFAULT", "tc-0")
    selenium_util.click_link_text("Dashboard")
    assert expected_value in selenium_util.driver.page_source, f"Expected value: {expected_value} not in page source."
