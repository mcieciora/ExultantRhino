def create_project(selenium_util, project_name, project_description):
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Select object type", "Project")
    selenium_util.write_input("Title", project_name)
    selenium_util.write_input("Description", project_description)
    selenium_util.submit_form()


def create_release(selenium_util, release_name, release_description, parent_project):
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", parent_project)
    selenium_util.choose_from_select_box("Select object type", "Release")
    selenium_util.write_input("Title", release_name)
    selenium_util.write_input("Description", release_description)
    selenium_util.submit_form()


def create_requirement(selenium_util, requirement_name, requirement_description, parent_project, parent_item):
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", parent_project)
    selenium_util.choose_from_select_box("Select object type", "Requirement")
    selenium_util.write_input("Title", requirement_name)
    selenium_util.write_input("Description", requirement_description)
    selenium_util.choose_from_select_box("Parent item", parent_item)
    selenium_util.submit_form()


def create_test_case(selenium_util, test_case_name, test_case_description, parent_project, parent_item):
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", parent_project)
    selenium_util.choose_from_select_box("Select object type", "Test case")
    selenium_util.write_input("Title", test_case_name)
    selenium_util.write_input("Description", test_case_description)
    selenium_util.choose_from_select_box("Parent item", parent_item)
    selenium_util.submit_form()


def create_bug(selenium_util, bug_name, bug_description, parent_project, parent_item):
    selenium_util.click_link_text("+Create")
    selenium_util.choose_from_select_box("Selected proj-0: DEFAULT. current_project", parent_project)
    selenium_util.choose_from_select_box("Select object type", "Bug")
    selenium_util.write_input("Title", bug_name)
    selenium_util.write_input("Description", bug_description)
    selenium_util.choose_from_select_box("Parent item", parent_item)
    selenium_util.submit_form()
