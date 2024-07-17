from os import environ
from re import findall
from pytest import mark
from automated_tests.streamlit_ui_util import create_release


@mark.nightly
def test__nightly__streamlit_app__items_page(empty_database_fixture_function, selenium_util):
    expected_items = ["<p>DEFAULT</p>", f"http://{environ['API_HOST']}:8501/+Create?item=proj-0",
                      "Selected No options to select.."]
    selenium_util.click_link_text("Items")
    for item in expected_items:
        assert item in selenium_util.driver.page_source, f"{item} not found in page source."
    create_release(selenium_util, "alpha", "alpha description", "DEFAULT")
    expected_items = ["<p>DEFAULT</p>", "<p>alpha</p>", f"http://{environ['API_HOST']}:8501/+Create?item=proj-0",
                      f"http://{environ['API_HOST']}:8501/+Create?item=rls-0", "Selected alpha"]
    selenium_util.click_link_text("Items")
    for item in expected_items:
        assert item in selenium_util.driver.page_source, f"{item} not found in page source."


@mark.nightly
def test__nightly__streamlit_app__items_page_multiple_releases(two_fully_set_up_projects, selenium_util):
    pattern = r"<p>req_\d</p>|<p>tc_\d</p>|<p>bug_tc_\d</p>"
    selenium_util.click_link_text("Items")
    expected_items = ["DEFAULT", "0_1"]
    for item in expected_items:
        assert item in selenium_util.driver.page_source, f"{item} not found in page source."
    expected_value = 6
    actual_value = len(findall(pattern, selenium_util.driver.page_source))
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
    selenium_util.choose_from_select_box("Selected 0_1. Filter by release", "0_2")
    expected_items = ["DEFAULT", "0_2"]
    for item in expected_items:
        assert item in selenium_util.driver.page_source, f"{item} not found in page source."
    expected_value = 4
    actual_value = len(findall(pattern, selenium_util.driver.page_source))
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.nightly
def test__nightly__streamlit_app__tasks_page_active_release(two_fully_set_up_projects, selenium_util):
    pattern = r"<p>Cover req-\d</p>|<p>Cover tc-\d</p>|<p>Cover bug-\d</p>"
    selenium_util.click_link_text("Releases")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project_select_box", "new_project")
    selenium_util.submit_form_by_text("Activate")
    selenium_util.click_link_text("Tasks")
    expected_value = 7
    actual_value = len(findall(pattern, selenium_util.driver.page_source))
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.nightly
def test__nightly__streamlit_app__tasks_page_verify_status_change(two_fully_set_up_projects, selenium_util):
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project_select_box", "new_project")
    for index, status in enumerate(["ToDo", "InProgress", "InReview", "Implemented"]):
        selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/Tasks?item=task-{index}")
        selenium_util.choose_from_select_box("Selected New. Status", status)
        selenium_util.submit_form()
    selenium_util.click_link_text("Dashboard")
    selenium_util.click_link_text("Tasks")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project_select_box", "new_project")
    accessible_text = "Selected All. Filter by status"
    for status, expected_value in {"New": 3, "ToDo": 1, "InProgress": 1, "InReview": 1, "Implemented": 1}.items():
        pattern = fr"<p>{status}</p>"
        selenium_util.choose_from_select_box(accessible_text, status)
        accessible_text = f"Selected {status}. Filter by status"
        actual_value = len(findall(pattern, selenium_util.driver.page_source))
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
