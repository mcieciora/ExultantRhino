from os import environ
from pytest import mark
from re import findall


@mark.smoke
def test__smoke__streamlit_app__edit_project(one_object_of_type_database_fixture, selenium_util):
    base_url = f"http://{environ['API_HOST']}:8501/+Create?item="
    test_data = {
        "project": {
            "item_shortname": "proj-0"
        },
        "release": {
            "item_shortname": "rls-0"
        },
        "requirement": {
            "item_shortname": "req-0"
        },
        "testcase": {
            "item_shortname": "tc-0"
        },
        "bug": {
            "item_shortname": "bug-0"
        }
    }
    for item_type, item_data in test_data.items():
        selenium_util.go_to_page(f"{base_url}{item_data['item_shortname']}")
        selenium_util.overwrite_value("Title", "edited title")
        selenium_util.overwrite_value("Description", "edited description")
        selenium_util.submit_form()
        assert findall(f"{item_data['item_shortname']}: new {item_type} was updated.",
                       selenium_util.driver.page_source), \
            f"{item_type.capitalize()} edition message not found."
