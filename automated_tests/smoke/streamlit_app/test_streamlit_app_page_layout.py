from os import environ
from pytest import mark


@mark.smoke
def test__smoke__streamlit_app__item_not_found(one_object_of_type_database_fixture, selenium_util):
    test_data = "proj-1"
    expected_value = "Item not found"
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/+Create?item={test_data}")
    assert expected_value in selenium_util.driver.page_source, "Item not found message not found."


@mark.smoke
def test__smoke__streamlit_app__task_not_found(one_object_of_type_database_fixture, selenium_util):
    test_data = "task-0"
    expected_value = "Task not found"
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/Tasks?item={test_data}")
    assert expected_value in selenium_util.driver.page_source, "Task not found message not found."


@mark.smoke
def test__smoke__streamlit_app__cached_project_select_box(two_projects_fixture, selenium_util):
    selenium_util.choose_from_select_box("Selected first project. current_project", "second project")
    for page in ["+Create", "Releases", "Tasks", "Items", "Results", "Dashboard"]:
        selenium_util.click_link_text(page)
        assert "Selected second project" in selenium_util.driver.page_source, f"Project was not cached for {page}"
    selenium_util.click_link_text("Configuration")
    selenium_util.click_link_text("Dashboard")
    assert "Selected first project" in selenium_util.driver.page_source, "Project was not reset to default"
