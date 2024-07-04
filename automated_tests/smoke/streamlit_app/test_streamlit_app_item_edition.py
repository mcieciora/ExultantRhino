from os import environ
from pytest import mark
from re import findall
from src.postgres_items_models import Bug, Requirement, TestCase
from src.postgres_sql_alchemy import get_objects_by_filters
from automated_tests.postgres_util import get_item_page_url_by_title


@mark.smoke
def test__smoke__streamlit_app__edit_items(one_object_of_type_database_fixture, selenium_util):
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/+Create?item=proj-0")
    selenium_util.overwrite_value("Title", "edited title")
    selenium_util.overwrite_value("Description", "edited description")
    assert findall(f"Project title cannot be edited.", selenium_util.driver.page_source), "Forbidden project edition " \
                                                                                          "message not found."
