from pytest import mark
from src.postgres_sql_alchemy import TestCase
from automated_tests.postgres_util import get_item_page_url_by_title


@mark.regression
def test__regression__streamlit_app__select_box_fails_to_gather_list_of_parent_items_when_different_project_is_set(
        two_fully_set_up_projects, selenium_util):
    test_page = get_item_page_url_by_title(TestCase, "t1")
    selenium_util.go_to_page(test_page)
    unwanted_value = "ValueError: 'req-3' is not in list"
    assert unwanted_value in selenium_util.driver.page_source, "Unwanted value found in page source."
