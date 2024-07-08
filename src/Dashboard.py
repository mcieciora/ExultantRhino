from streamlit import columns, header, sidebar, metric, write
from src.postgres_items_models import Bug, Project, Release, Requirement, TestCase
from src.postgres_sql_alchemy import get_all_objects_by_type, get_objects_by_filters, init_db

init_db()


def find_projects():
    """
    Get all available projects in list format.

    :return: List of Project database objects.
    """
    all_projects = get_all_objects_by_type(Project)
    return [f"{db_object['shortname']}: {db_object['title']}" for db_object in all_projects]


current_project = sidebar.selectbox(
    label="current_project",
    key="current_project",
    options=find_projects(),
    index=0,
    placeholder="Select project...",
    label_visibility="collapsed",
)


header("Dashboard")
releases_col, requirements_col, testcases_col, bugs_col = columns(4)

releases = get_objects_by_filters(Release, {"project_shortname": current_project.split(':')[0]})
requirements = get_objects_by_filters(Requirement, {"project_shortname": current_project.split(':')[0]})
test_cases = get_objects_by_filters(TestCase, {"project_shortname": current_project.split(':')[0]})
bugs = get_objects_by_filters(Bug, {"project_shortname": current_project.split(':')[0]})

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

if len(bugs) > 0:
    write(f"There are {len(bugs)} active bugs.")
