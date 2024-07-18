from pytest import mark
from re import findall


@mark.smoke
def test__smoke__streamlit_app__create_project(empty_database_fixture_session, selenium_util):
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
    expected_value = None
    assert "Selected Project. Select object type" in selenium_util.driver.page_source, "Select object type select " \
                                                                                       "box not found"
    for form_field in ["Title", "Description", "Project Shortname", "Project"]:
        assert expected_value == selenium_util.find_element_by_xpath_accessible_text(form_field), \
            f"Found {form_field} after form submission."


@mark.smoke
def test__smoke__streamlit_app__forbid_to_create_project_with_same_title(empty_database_fixture_session, selenium_util):
    test_data = {
        "item_name": "new_proj",
        "item_description": "new_proj description"
    }
    expected_value = "Project with title: new_proj already exists."
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Select object type", "Project")
    selenium_util.write_input("Title", test_data["item_name"])
    selenium_util.write_input("Description", test_data["item_description"])
    selenium_util.submit_form()
    assert expected_value in selenium_util.driver.page_source, "Forbidden project creation message not found."
