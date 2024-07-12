from os import environ
from pytest import mark
from re import findall


@mark.skip("Feature not yet implemented")
@mark.smoke
def test__smoke__streamlit_app__edit_items(one_object_of_type_database_fixture, selenium_util):
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/+Create?item=proj-0")
    selenium_util.overwrite_value("Title", "edited title")
    selenium_util.overwrite_value("Description", "edited description")
    assert findall("Project title cannot be edited.", selenium_util.driver.page_source), "Forbidden project edition " \
                                                                                         "message not found."
