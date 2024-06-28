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


@mark.nightly
def test__smoke__streamlit_app__create_release(empty_database_fixture_session, selenium_util):
    test_data = {
        "item_name": "first_release",
        "item_description": "first_release description",
        "item_parent_project": "new_proj"
    }
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", test_data["item_parent_project"])
    selenium_util.choose_from_select_box("Select object type", "Release")
    selenium_util.write_input("Title", test_data["item_name"])
    selenium_util.write_input("Description", test_data["item_description"])
    selenium_util.submit_form()
    assert findall(r"Created rls-\d+", selenium_util.driver.page_source), "Release creation message not found."


@mark.nightly
def test__smoke__streamlit_app__create_requirement(empty_database_fixture_session, selenium_util):
    test_data = {
        "item_name": "first_requirement",
        "item_description": "first_requirement description",
        "item_parent_project": "new_proj",
        "item_parent_object": "rls-0"
    }
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", test_data["item_parent_project"])
    selenium_util.choose_from_select_box("Select object type", "Requirement")
    selenium_util.write_input("Title", test_data["item_name"])
    selenium_util.write_input("Description", test_data["item_description"])
    selenium_util.choose_from_select_box("Parent item", test_data["item_parent_object"])
    selenium_util.submit_form()
    assert findall(r"Created req-\d+", selenium_util.driver.page_source), "Release creation message not found."


@mark.nightly
def test__smoke__streamlit_app__create_test_case(empty_database_fixture_session, selenium_util):
    test_data = {
        "item_name": "test_case",
        "item_description": "test_case description",
        "item_parent_project": "new_proj",
        "item_parent_object": "req-0"
    }
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", test_data["item_parent_project"])
    selenium_util.choose_from_select_box("Select object type", "Test case")
    selenium_util.write_input("Title", test_data["item_name"])
    selenium_util.write_input("Description", test_data["item_description"])
    selenium_util.choose_from_select_box("Parent item", test_data["item_parent_object"])
    selenium_util.submit_form()
    assert findall(r"Created tc-\d+", selenium_util.driver.page_source), "Release creation message not found."


@mark.nightly
def test__smoke__streamlit_app__create_bug(empty_database_fixture_session, selenium_util):
    test_data = {
        "item_name": "bug",
        "item_description": "bug description",
        "item_parent_project": "new_proj",
        "item_parent_object": "tc-0"
    }
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", test_data["item_parent_project"])
    selenium_util.choose_from_select_box("Select object type", "Bug")
    selenium_util.write_input("Title", test_data["item_name"])
    selenium_util.write_input("Description", test_data["item_description"])
    selenium_util.choose_from_select_box("Parent item", test_data["item_parent_object"])
    selenium_util.submit_form()
    assert findall(r"Created bug-\d+", selenium_util.driver.page_source), "Bug creation message not found."
