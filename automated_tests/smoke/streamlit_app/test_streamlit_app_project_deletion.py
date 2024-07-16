from os import environ
from time import sleep
from pytest import mark
from src.postgres_items_models import Project
from automated_tests.postgres_util import get_item_page_url_by_title


DELETION_WAIT = 0.75


@mark.smoke
def test__smoke__streamlit_app__delete_protected_default_project(two_fully_set_up_projects, selenium_util):
    expected_value = "DEFAULT project cannot be deleted."
    test_page = get_item_page_url_by_title(Project, "DEFAULT")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete")
    assert expected_value in selenium_util.driver.page_source, "DEFAULT project forbidden deletion message not found"


@mark.smoke
def test__smoke__streamlit_app__delete_project(two_fully_set_up_projects, selenium_util):
    expected_value = "Deleted new_project, 8 related items and 0 tasks"
    test_page = get_item_page_url_by_title(Project, "new_project")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete", wait_for_load=False)
    sleep(DELETION_WAIT)
    assert expected_value in selenium_util.driver.page_source, "DEFAULT project forbidden deletion message not found"


@mark.smoke
def test__smoke__streamlit_app__delete_selected_project(multiple_not_covered_items, selenium_util):
    test_page = get_item_page_url_by_title(Project, "new_project")
    selenium_util.go_to_page(test_page)
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project_select_box", "new_project")
    selenium_util.submit_form_by_text("Delete")
    sleep(DELETION_WAIT)
    project_select_box = selenium_util.find_element_by_xpath_accessible_text("Selected DEFAULT. "
                                                                             "current_project_select_box")
    assert project_select_box, "Selected project was not reset to DEFAULT."
    assert f"http://{environ['API_HOST']}:8501/Items" == selenium_util.driver.current_url, \
        "User was not redirected to Dashboard page."


@mark.smoke
def test__smoke__streamlit_app__delete_project_and_related_tasks(multiple_not_covered_items, selenium_util):
    expected_value = "Deleted new_project, 17 related items and 13 tasks"
    selenium_util.click_link_text("Releases")
    selenium_util.choose_from_select_box("Selected DEFAULT. current_project_select_box", "new_project")
    selenium_util.submit_form_by_text("Activate")
    test_page = get_item_page_url_by_title(Project, "new_project")
    selenium_util.go_to_page(test_page)
    selenium_util.submit_form_by_text("Delete", wait_for_load=False)
    sleep(DELETION_WAIT)
    assert expected_value in selenium_util.driver.page_source, "DEFAULT project forbidden deletion message not found"
