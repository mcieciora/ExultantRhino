from os import environ
from pytest import mark
from re import findall
from src.postgres_items_models import Bug, Requirement, TestCase
from src.postgres_sql_alchemy import get_objects_by_filters
from automated_tests.postgres_util import get_item_page_url_by_title


@mark.smoke
def test__smoke__streamlit_app__edit_items(one_object_of_type_database_fixture, selenium_util):
    test_data = {
        "project": "proj-0",
        "release": "rls-0",
        "requirement": "req-0",
        "testcase": "tc-0",
        "bug": "bug-0"
    }
    for item_type, item_shortname in test_data.items():
        selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/+Create?item={item_shortname}")
        selenium_util.overwrite_value("Title", "edited title")
        selenium_util.overwrite_value("Description", "edited description")
        selenium_util.submit_form()
        assert findall(f"{item_shortname}: new {item_type} was updated.",
                       selenium_util.driver.page_source), \
            f"{item_type.capitalize()} edition message not found."


@mark.nightly
def test__nightly__streamlit_app__change_parent_release(two_fully_set_up_projects, selenium_util):
    requirement_page = get_item_page_url_by_title(Requirement, "req_1")
    expected_value = "rls-1"
    selenium_util.go_to_page(requirement_page)
    selenium_util.choose_from_select_box("Selected rls-0: 0_1. Parent item", "0_2")
    selenium_util.submit_form()

    affected_items = [(TestCase, "tc_1"), (TestCase, "tc_2"), (Bug, "bug_tc_2")]

    db_item = get_objects_by_filters(Requirement, {"title": "req_1"})[0]
    actual_value = db_item["parent"]
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in affected_items:
        db_item = get_objects_by_filters(item[0], {"title": item[1]})[0]
        actual_value = db_item["target_release"]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    actual_value = len(get_objects_by_filters(Requirement, {"target_release": "rls-1"}))
    expected_value = 2
    assert actual_value == expected_value, f"Expected: {actual_value}, actual: {expected_value}"

    actual_value = len(get_objects_by_filters(TestCase, {"target_release": "rls-1"}))
    expected_value = 4
    assert actual_value == expected_value, f"Expected: {actual_value}, actual: {expected_value}"

    actual_value = len(get_objects_by_filters(Bug, {"target_release": "rls-1"}))
    expected_value = 2
    assert actual_value == expected_value, f"Expected: {actual_value}, actual: {expected_value}"


@mark.nightly
def test__nightly__streamlit_app__change_parent_requirement(two_fully_set_up_projects, selenium_util):
    test_case_page = get_item_page_url_by_title(TestCase, "tc_4")
    expected_value = "req-1"
    selenium_util.go_to_page(test_case_page)
    selenium_util.choose_from_select_box("Selected req-2: req_3. Parent item", "req_2")
    selenium_util.submit_form()

    affected_items = [(Bug, "bug_tc_4")]

    db_item = get_objects_by_filters(TestCase, {"title": "tc_4"})[0]
    actual_value = db_item["parent"]
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in affected_items:
        db_item = get_objects_by_filters(item[0], {"title": item[1]})[0]
        expected_value = "rls-0"
        actual_value = db_item["target_release"]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    actual_value = len(get_objects_by_filters(Requirement, {"target_release": "rls-0"}))
    expected_value = 1
    assert actual_value == expected_value, f"Expected: {actual_value}, actual: {expected_value}"

    actual_value = len(get_objects_by_filters(TestCase, {"target_release": "rls-0"}))
    expected_value = 2
    assert actual_value == expected_value, f"Expected: {actual_value}, actual: {expected_value}"

    actual_value = len(get_objects_by_filters(Bug, {"target_release": "rls-0"}))
    expected_value = 1
    assert actual_value == expected_value, f"Expected: {actual_value}, actual: {expected_value}"


@mark.nightly
def test__nightly__streamlit_app__change_parent_test_case(two_fully_set_up_projects, selenium_util):
    test_case_page = get_item_page_url_by_title(Bug, "bug_tc_4")
    expected_value = "tc-0"
    selenium_util.go_to_page(test_case_page)
    selenium_util.choose_from_select_box("Selected tc-3: tc_4. Parent item", "tc_1")
    selenium_util.submit_form()

    item = (Bug, "bug_tc_4")

    db_item = get_objects_by_filters(Bug, {"title": "bug_tc_4"})[0]
    actual_value = db_item["parent"]
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    db_item = get_objects_by_filters(item[0], {"title": item[1]})[0]
    expected_value = "rls-1"
    actual_value = db_item["target_release"]
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    actual_value = len(get_objects_by_filters(Requirement, {"target_release": "rls-1"}))
    expected_value = 2
    assert actual_value == expected_value, f"Expected: {actual_value}, actual: {expected_value}"

    actual_value = len(get_objects_by_filters(TestCase, {"target_release": "rls-1"}))
    expected_value = 3
    assert actual_value == expected_value, f"Expected: {actual_value}, actual: {expected_value}"

    actual_value = len(get_objects_by_filters(Bug, {"target_release": "rls-1"}))
    expected_value = 2
    assert actual_value == expected_value, f"Expected: {actual_value}, actual: {expected_value}"
