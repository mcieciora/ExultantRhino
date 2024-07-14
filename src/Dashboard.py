from streamlit import columns, container, divider, header, session_state, sidebar, metric, write
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
releases_col, requirements_col, testcases_col, bugs_col = columns(4)

releases = get_objects_by_filters(Release, {"project_shortname": session_state.current_project})
requirements = get_objects_by_filters(Requirement, {"project_shortname": session_state.current_project})
test_cases = get_objects_by_filters(TestCase, {"project_shortname": session_state.current_project})
bugs = get_objects_by_filters(Bug, {"project_shortname": session_state.current_project})

with releases_col:
    metric(
        label="Releases",
        value=len(
            releases
        ),
    )

with requirements_col:
    metric(
        label="Requirements",
        value=len(
            requirements
        ),
    )

with testcases_col:
    metric(
        label="Test cases",
        value=len(
            test_cases
        ),
    )

with bugs_col:
    metric(
        label="Bugs",
        value=len(
            bugs
        ),
    )

not_covered_releases = [release for release in releases
                        if not list(filter(lambda x: x["target_release"] == release["shortname"], requirements))]
not_covered_requirements = [requirement for requirement in requirements
                            if not list(filter(lambda x: x["parent"] == requirement["shortname"], test_cases))]
if (releases_length := len(not_covered_releases)) > 0:
    with container(border=True):
        write(f":blue[Notification.] There {'are' if releases_length > 1 else 'is'} {releases_length} empty "
              f"{'releases' if releases_length > 1 else 'release'}.")
if (requirements_length := len(not_covered_requirements)) > 0:
    with container(border=True):
        write(f":blue[Notification.] There {'are' if requirements_length > 1 else 'is'} {requirements_length} "
              f"{'requirements' if requirements_length > 1 else 'requirement'} not covered with test cases.")
if (bugs_length := len(bugs)) > 0:
    with container(border=True):
        write(f":blue[Notification.] There {'are' if bugs_length > 1 else 'is'} {bugs_length} active "
              f"{'bugs' if bugs_length > 1 else 'bug'}.")

divider()
