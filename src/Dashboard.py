from streamlit import columns, header, session_state, sidebar, metric
from src.postgres_items_models import Bug, Project, Release, Requirement, TestCase
from src.postgres_sql_alchemy import get_all_objects_by_type, get_objects_by_filters, init_db

init_db()


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


header("Dashboard")
releases, requirements, testcases, bugs = columns(4)

with releases:
    metric(
        label="Releases",
        value=len(
            get_objects_by_filters(Release, {"project_shortname": session_state.current_project})
        ),
    )

with requirements:
    metric(
        label="Requirements",
        value=len(
            get_objects_by_filters(Requirement, {"project_shortname": session_state.current_project})
        ),
    )

with testcases:
    metric(
        label="Test cases",
        value=len(
            get_objects_by_filters(TestCase, {"project_shortname": session_state.current_project})
        ),
    )

with bugs:
    metric(
        label="Bugs",
        value=len(
            get_objects_by_filters(Bug, {"project_shortname": session_state.current_project})
        ),
    )
