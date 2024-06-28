from pytest import mark
from src.postgres_items_models import Bug, Requirement, TestCase
from src.postgres_sql_alchemy import get_all_objects
from automated_tests.postgres_util import get_item_page_url_by_title


@mark.nightly
def test__smoke__streamlit_app__delete_requirement(two_fully_set_up_projects, selenium_util):
    test_page = get_item_page_url_by_title(Requirement, "req_2")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete")

    affected_items = ["req_2", "tc_3"]

    actual_items = [item["title"] for item in get_all_objects()]

    for item in affected_items:
        assert item not in actual_items, f"Expected key: {item} does exist. {actual_items}"


@mark.nightly
def test__smoke__streamlit_app__delete_test_case(two_fully_set_up_projects, selenium_util):
    test_page = get_item_page_url_by_title(TestCase, "tc_1")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete")

    affected_items = ["tc_1"]

    actual_items = [item["title"] for item in get_all_objects()]

    for item in affected_items:
        assert item not in actual_items, f"Expected key: {item} does exist. {actual_items}"


@mark.nightly
def test__smoke__streamlit_app__delete_bug(two_fully_set_up_projects, selenium_util):
    test_page = get_item_page_url_by_title(Bug, "bug_tc_2")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete")

    affected_items = ["bug_tc_2"]

    actual_items = [item["title"] for item in get_all_objects()]

    for item in affected_items:
        assert item not in actual_items, f"Expected key: {item} does exist. {actual_items}"
