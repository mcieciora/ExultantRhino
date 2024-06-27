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
