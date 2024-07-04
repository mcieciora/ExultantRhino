from pytest import mark
from re import findall


@mark.smoke
def test__smoke__streamlit_app__create_project(empty_database_fixture_function, selenium_util):
    test_data = {
        "item_name": "new_proj",
        "item_description": "new_proj description"
    }
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Select object type", "Project")
    selenium_util.write_input("Title", test_data["item_name"])
    selenium_util.write_input("Description", test_data["item_description"])
    selenium_util.submit_form()
    assert findall(r"Created proj-\d+", selenium_util.driver.page_source), "Project creation message not found."
