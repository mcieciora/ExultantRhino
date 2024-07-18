from os.path import exists
from streamlit import file_uploader, markdown, session_state, sidebar, subheader, success, tabs
from src.postgres_items_models import Project
from src.postgres_sql_alchemy import get_all_objects_by_type


def find_projects():
    """
    Get all available projects in list format.

    :return: List of Project database objects.
    """
    return [f"{db_object['title']}" for db_object in get_all_objects_by_type(Project)]


all_projects = find_projects()
session_state.current_project = sidebar.selectbox(
    label="current_project_select_box",
    key="current_project_select_box",
    options=all_projects,
    index=all_projects.index(session_state["current_project"]) if "current_project" in session_state else 0,
    placeholder="Select project...",
    label_visibility="collapsed",
)

project_md_file = f"{session_state.current_project.replace(' ', '_')}_README.md"
markdown_tab, upload_tab = tabs(["View documentation", "Upload documentation"])


def read_md_file(md_file):
    """
    Open markdown file and get file content in bytes.

    :return: File bytes data.
    """
    with open(md_file, mode="r") as file:
        return file.read()


with markdown_tab:
    if exists(project_md_file):
        intro_markdown = read_md_file(project_md_file)
        markdown(intro_markdown, unsafe_allow_html=True)
    else:
        subheader("No documentation uploaded.")

with upload_tab:
    uploaded_file = file_uploader(label="Choose markdown file")
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        with open(project_md_file, mode="wb") as markdown_file:
            markdown_file.write(bytes_data)
            success(f"Uploaded {uploaded_file.name}")
