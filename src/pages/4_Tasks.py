from requests import get
from streamlit import header, sidebar


def find_projects():
    """
    Get all available projects in list format.
    :return: List of Project database objects.
    """
    all_projects = get("http://exultant_rhino_api:8101/get_objects/project", timeout=5)
    return [db_object['title'] for db_object in all_projects.json()]


current_project = sidebar.selectbox(
    label="current_project",
    key="current_project",
    options=find_projects(),
    index=0,
    placeholder="Select project...",
    label_visibility="collapsed",
)

header("Tasks")
