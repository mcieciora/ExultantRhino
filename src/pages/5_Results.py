from streamlit import header, session_state, sidebar
from src.postgres_items_models import Project
from src.postgres_sql_alchemy import get_all_objects_by_type


def find_projects():
    """
    Get all available projects in list format.

    :return: List of Project database objects.
    """
    return [f"{db_object['title']}" for db_object in get_all_objects_by_type(Project)]


all_projects = find_projects()
current_project = sidebar.selectbox(
    label="current_project",
    key="current_project",
    options=all_projects,
    index=all_projects.index(session_state.current_project) if "current_project" in session_state else 0,
    placeholder="Select project...",
    label_visibility="collapsed",
)

header("Results")
