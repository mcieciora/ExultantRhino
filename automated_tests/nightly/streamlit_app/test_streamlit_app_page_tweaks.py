from os import environ
from pytest import mark
from src.postgres_sql_alchemy import TestCase
from automated_tests.postgres_util import get_item_page_url_by_title


@mark.nightly
def test__nightly__streamlit_app__item_not_found(one_object_of_type_database_fixture, selenium_util):
    test_data = "proj-1"
    expected_value = "Item not found"
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/+Create?item={test_data}")
    assert expected_value in selenium_util.driver.page_source, "Item not found message not found."


@mark.nightly
def test__nightly__streamlit_app__task_not_found(one_object_of_type_database_fixture, selenium_util):
    test_data = "task-0"
    expected_value = "Task not found"
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/Tasks?item={test_data}")
    assert expected_value in selenium_util.driver.page_source, "Task not found message not found."


@mark.nightly
def test__nightly__streamlit_app__cached_project_select_box(two_projects_fixture, selenium_util):
    selenium_util.choose_from_select_box("Selected first project. current_project_select_box", "second project")
    for page in ["+Create", "Releases", "Tasks", "Items", "Dashboard"]:
        selenium_util.click_link_text(page)
        assert "Selected second project" in selenium_util.driver.page_source, f"Project was not cached for {page}"
    selenium_util.choose_from_select_box("Selected second project. current_project_select_box", "first project")
    selenium_util.click_link_text("+Create")
    assert "Selected first project" in selenium_util.driver.page_source, "Project was not reset to default"


@mark.nightly
def test__nightly_streamlit_app__project_select_box_disabled_enabled(one_object_of_type_database_fixture,
                                                                     selenium_util):
    test_data = "rls-0"
    selenium_util.click_link_text("+Create")
    project_select_box = selenium_util.find_element_by_xpath_accessible_text("Selected new project. "
                                                                             "current_project_select_box")
    expected_value = True
    assert expected_value == project_select_box.is_enabled()
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/+Create?item={test_data}")
    project_select_box = selenium_util.find_element_by_xpath_accessible_text("Selected new project. "
                                                                             "current_project_select_box")
    expected_value = False
    assert expected_value == project_select_box.is_enabled()


@mark.nightly
@mark.regression
def test__nightly__streamlit_app__select_box_fails_to_gather_list_of_parent_items_when_different_project_is_set(
        two_fully_set_up_projects, selenium_util):
    expected_value = False
    test_page = get_item_page_url_by_title(TestCase, "t1")
    selenium_util.go_to_page(test_page)
    project_select_box = selenium_util.find_element_by_xpath_accessible_text("Selected new_project. "
                                                                             "current_project_select_box")
    assert project_select_box, "Expected select box element not found."
    assert expected_value == project_select_box.is_enabled(), "Project select box is enabled."
