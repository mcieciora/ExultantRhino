from os import environ
from re import findall
from pytest import mark
from automated_tests.streamlit_ui_util import create_bug, create_requirement


@mark.nightly
def test__nightly__streamlit_app__activate_release(two_fully_set_up_projects, selenium_util):
    selenium_util.click_link_text("Releases")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project", "new_project")
    selenium_util.submit_form_by_text("Activate")
    assert "Release alpha is active now." in selenium_util.driver.page_source, \
        "Expected release activation info not available"

    assert "Current release: alpha" in selenium_util.driver.page_source, "Expected release info not available"

    expected_values = ["2", "3", "2", "Active"]
    for index, actual_value in \
            enumerate(selenium_util.find_elements_by_xpath_accessible_text("stMetricValue", "data-testid")):
        expected_value = expected_values[index]
        assert expected_value == actual_value.text, f"Expected value: {expected_value} does not equal {actual_value}"

    expected_task_completion_percentage = "Completion: 0.0%"
    assert expected_task_completion_percentage in selenium_util.driver.page_source, \
        f"Expected: {expected_task_completion_percentage} not found in page source."


@mark.nightly
def test__nightly__streamlit_app__check_generated_tasks(two_fully_set_up_projects, selenium_util):
    selenium_util.click_link_text("Tasks")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project", "new_project")

    expected_items = ["Cover req-3", "Cover req-4", "Cover tc-5", "Cover tc-6", "Cover tc-7", "Cover bug-2",
                      "Cover bug-3"]
    for expected_item in expected_items:
        assert expected_item in selenium_util.driver.page_source, f"Expected: {expected_item} not found in page source"


@mark.nightly
def test__nightly__streamlit_app__refresh_release(two_fully_set_up_projects, selenium_util):
    create_requirement(selenium_util, "Additional requirement", "Additional requirement description", "new_project",
                       "rls-2")
    selenium_util.click_link_text("Releases")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project", "new_project")

    selenium_util.submit_form_by_text("Refresh")

    assert "All tasks were updated." in selenium_util.driver.page_source, "Expected release update info not available"

    selenium_util.click_link_text("Tasks")

    expected_items = ["Cover req-3", "Cover req-4", "Cover req-5", "Cover tc-5", "Cover tc-6", "Cover tc-7",
                      "Cover bug-2", "Cover bug-3"]
    for expected_item in expected_items:
        assert expected_item in selenium_util.driver.page_source, f"Expected: {expected_item} not found in page source"


@mark.nightly
def test__nightly__streamlit_app__change_task_status(two_fully_set_up_projects, selenium_util):
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/Tasks?item=task-0")
    selenium_util.choose_from_select_box("Selected New. Status", "ToDo")
    selenium_util.submit_form()
    assert findall("Updated Cover req-3", selenium_util.driver.page_source), "Task update message not found."


@mark.nightly
def test__nightly__streamlit_app__verify_completion_percentage(two_fully_set_up_projects, selenium_util):
    for task_index in range(1, 8):
        selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/Tasks?item=task-{task_index}")
        selenium_util.choose_from_select_box("Selected New. Status", "Implemented")
        selenium_util.submit_form()
        selenium_util.click_link_text("Releases")
        selenium_util.choose_from_select_box("Selected DEFAULT. current_project", "new_project")
        expected_task_completion_percentage = f"Completion: {task_index*12.5}%"
        assert expected_task_completion_percentage in selenium_util.driver.page_source, \
            f"Expected: {expected_task_completion_percentage} not found in page source."


@mark.nightly
def test__nightly__streamlit_app__add_new_item_and_finish_release(two_fully_set_up_projects, selenium_util):
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/Tasks?item=task-0")
    selenium_util.choose_from_select_box("Selected ToDo. Status", "Implemented")
    selenium_util.submit_form()
    create_bug(selenium_util, "Additional bug", "Additional bug description", "new_project", "tc-1")
    selenium_util.click_link_text("Releases")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project", "new_project")
    expected_task_completion_percentage = "Completion: 100.0%"
    assert expected_task_completion_percentage in selenium_util.driver.page_source, \
        f"Expected: {expected_task_completion_percentage} not found in page source."
    selenium_util.submit_form_by_text("Finish")
    expected_message = "Not all items are covered with tasks. Please use Refresh button."
    assert expected_message in selenium_util.driver.page_source, \
        f"Expected: {expected_message} not found in page source."


@mark.nightly
def test__nightly__streamlit_app__refresh_release_on_full_completion(two_fully_set_up_projects, selenium_util):
    selenium_util.click_link_text("Releases")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project", "new_project")
    selenium_util.submit_form_by_text("Refresh")
    expected_task_completion_percentage = "Completion: 88.89%"
    assert expected_task_completion_percentage in selenium_util.driver.page_source, \
        f"Expected: {expected_task_completion_percentage} not found in page source."
    selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/Tasks?item=task-8")
    selenium_util.choose_from_select_box("Selected New. Status", "Implemented")
    selenium_util.submit_form()
    selenium_util.click_link_text("Releases")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project", "new_project")
    expected_task_completion_percentage = "Completion: 100.0%"
    assert expected_task_completion_percentage in selenium_util.driver.page_source, \
        f"Expected: {expected_task_completion_percentage} not found in page source."


@mark.nightly
def test__nightly__streamlit_app__finish_release_on_full_completion(two_fully_set_up_projects, selenium_util):
    selenium_util.click_link_text("Releases")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project", "new_project")
    selenium_util.submit_form_by_text("Finish")
    assert "Successfully finished release." in selenium_util.driver.page_source, "Expected release completion" \
                                                                                 " info not available"
    expected_values = ["3", "3", "3", "Implemented"]
    for index, actual_value in \
            enumerate(selenium_util.find_elements_by_xpath_accessible_text("stMetricValue", "data-testid")):
        expected_value = expected_values[index]
        assert expected_value == actual_value.text, f"Expected value: {expected_value} does not equal {actual_value}"


@mark.nightly
def test__nightly__streamlit_app__multiple_releases_activation(two_fully_set_up_projects, selenium_util):
    selenium_util.click_link_text("Releases")
    selenium_util.submit_form_by_text("Activate")
    assert "Activate" not in selenium_util.driver.page_source, "Expected: Activate found in page source."
    selenium_util.click_link_text("Tasks")
    expected_number_of_tasks = 7
    actual_number_of_tasks = len(findall(r'aria-rowindex="\d+"', selenium_util.driver.page_source))
    assert expected_number_of_tasks == actual_number_of_tasks, \
        f"Expected value: {expected_number_of_tasks} does not equal {actual_number_of_tasks}"


@mark.nightly
def test__nightly__streamlit_app__finish_multiple_releases(two_fully_set_up_projects, selenium_util):
    for task_index in range(9, 15):
        selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/Tasks?item=task-{task_index}")
        selenium_util.choose_from_select_box("Selected New. Status", "Implemented")
        selenium_util.submit_form()
    selenium_util.click_link_text("Releases")
    selenium_util.submit_form_by_text("Finish")
    selenium_util.submit_form_by_text("Activate")
    selenium_util.click_link_text("Tasks")
    expected_number_of_tasks = 5
    actual_number_of_tasks = len(findall(r'aria-rowindex="\d+"', selenium_util.driver.page_source))
    assert expected_number_of_tasks == actual_number_of_tasks, \
        f"Expected value: {expected_number_of_tasks} does not equal {actual_number_of_tasks}"
    for task_index in range(15, 19):
        selenium_util.go_to_page(f"http://{environ['API_HOST']}:8501/Tasks?item=task-{task_index}")
        selenium_util.choose_from_select_box("Selected New. Status", "Implemented")
        selenium_util.submit_form()
    selenium_util.click_link_text("Tasks")
    expected_number_of_tasks = 0
    actual_number_of_tasks = len(findall(r'aria-rowindex="\d+"', selenium_util.driver.page_source))
    assert expected_number_of_tasks == actual_number_of_tasks, \
        f"Expected value: {expected_number_of_tasks} does not equal {actual_number_of_tasks}"
    assert "No active release." not in selenium_util.driver.page_source, \
        "Expected: No active release. found in page source."
