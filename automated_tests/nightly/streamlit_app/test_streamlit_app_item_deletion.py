from pytest import mark
from src.postgres_items_models import Bug, Requirement, TestCase
from src.postgres_sql_alchemy import get_all_objects
from automated_tests.postgres_util import get_item_page_url_by_title


@mark.nightly
def test__nightly__streamlit_app__delete_requirement(two_fully_set_up_projects, selenium_util):
    test_page = get_item_page_url_by_title(Requirement, "req_2")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete")

    assert "Items" in selenium_util.driver.current_url, "User was not redirected to Items page."

    affected_items = ["req_2", "tc_3"]

    actual_items = [item["title"] for item in get_all_objects()]

    for item in affected_items:
        assert item not in actual_items, f"Expected key: {item} does exist. {actual_items}"


@mark.nightly
def test__nightly__streamlit_app__delete_test_case(two_fully_set_up_projects, selenium_util):
    test_page = get_item_page_url_by_title(TestCase, "tc_1")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete")

    assert "Items" in selenium_util.driver.current_url, "User was not redirected to Items page."

    affected_items = ["tc_1"]

    actual_items = [item["title"] for item in get_all_objects()]

    for item in affected_items:
        assert item not in actual_items, f"Expected key: {item} does exist. {actual_items}"


@mark.nightly
def test__nightly__streamlit_app__delete_bug(two_fully_set_up_projects, selenium_util):
    test_page = get_item_page_url_by_title(Bug, "bug_tc_2")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete")

    assert "Items" in selenium_util.driver.current_url, "User was not redirected to Items page."

    affected_items = ["bug_tc_2"]

    actual_items = [item["title"] for item in get_all_objects()]

    for item in affected_items:
        assert item not in actual_items, f"Expected key: {item} does exist. {actual_items}"


@mark.nightly
def test__nightly__streamlit_app__delete_task_and_verify_task_deletion(two_fully_set_up_projects, selenium_util):
    selenium_util.click_link_text("Releases")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project", "new_project")
    selenium_util.submit_form_by_text("Activate")
    test_page = get_item_page_url_by_title(TestCase, "t1")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete")
    selenium_util.click_link_text("Tasks")
    affected_item = "task-2"
    assert affected_item not in selenium_util.driver.page_source, f"{affected_item} found in page source."
