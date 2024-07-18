from os import getcwd
from os.path import join
from pytest import mark


@mark.nightly
def test__nightly__streamlit_app__upload_documentation(two_projects_fixture, selenium_util):
    header_content = "This is md file used for testing purposes only."
    expected_value = "No documentation uploaded."
    file_name = "test_md_file_1.md"
    selenium_util.click_link_text("Documentation")
    md_file_path = join(getcwd(), "automated_tests", "utils", "test_md_files", file_name)
    assert expected_value in selenium_util.driver.page_source, f"{expected_value} not found in page source."
    selenium_util.upload_file(md_file_path)
    assert f"Uploaded {file_name}" in selenium_util.driver.page_source, "Uploaded info not found in page source."
    selenium_util.refresh_and_wait()
    expected_content = f"Name of the file is: {file_name}"
    assert header_content in selenium_util.driver.page_source, f"{header_content} not found in page source."
    assert expected_content in selenium_util.driver.page_source, f"{expected_content} not found in page source."


@mark.nightly
def test__nightly__streamlit_app__upload_documentation_to_second_page(two_projects_fixture, selenium_util):
    header_content = "This is md file used for testing purposes only."
    expected_value = "No documentation uploaded."
    file_name = "test_md_file_2.md"
    selenium_util.click_link_text("Documentation")
    md_file_path = join(getcwd(), "automated_tests", "utils", "test_md_files", file_name)
    selenium_util.choose_from_select_box("Selected first project. current_project_select_box", "second project")
    assert expected_value in selenium_util.driver.page_source, f"{expected_value} not found in page source."
    selenium_util.upload_file(md_file_path)
    assert f"Uploaded {file_name}" in selenium_util.driver.page_source, "Uploaded info not found in page source."
    selenium_util.refresh_and_wait()
    selenium_util.choose_from_select_box("Selected first project. current_project_select_box", "second project")
    expected_content = f"Name of the file is: {file_name}"
    assert header_content in selenium_util.driver.page_source, f"{header_content} not found in page source."
    assert expected_content in selenium_util.driver.page_source, f"{expected_content} not found in page source."


@mark.nightly
def test__nightly__streamlit_app__overwrite_documentation(two_projects_fixture, selenium_util):
    header_content = "This is md file used for testing purposes only."
    file_name = "test_md_file_3.md"
    selenium_util.click_link_text("Documentation")
    md_file_path = join(getcwd(), "automated_tests", "utils", "test_md_files", file_name)
    selenium_util.upload_file(md_file_path)
    assert f"Uploaded {file_name}" in selenium_util.driver.page_source, "Uploaded info not found in page source."
    selenium_util.refresh_and_wait()
    expected_content = f"Name of the file is: {file_name}"
    assert header_content in selenium_util.driver.page_source, f"{header_content} not found in page source."
    assert expected_content in selenium_util.driver.page_source, f"{expected_content} not found in page source."
