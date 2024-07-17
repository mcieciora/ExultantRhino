from pytest import mark
from src.postgres_items_models import Release
from src.postgres_sql_alchemy import get_all_objects
from automated_tests.postgres_util import get_item_page_url_by_title


@mark.smoke
@mark.regression
def test__smoke__streamlit_app__delete_release(two_fully_set_up_projects, selenium_util):
    test_page = get_item_page_url_by_title(Release, "0_2")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete")
    assert "Items" in selenium_util.driver.current_url, "User was not redirected to Items page."
    affected_items = ["0_2", "req_3", "tc_4", "tc_5", "bug_tc_4"]
    actual_items = [item["title"] for item in get_all_objects()]
    for item in affected_items:
        assert item not in actual_items, f"Expected key: {item} does exist. {actual_items}"
