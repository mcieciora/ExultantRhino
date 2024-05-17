from streamlit import columns, header, sidebar, metric
from postgres_items_models import Bug, Project, Release, Requirement, TestCase
from postgres_sql_alchemy import get_all_objects_by_type, get_objects_by_filters


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
releases, requirements, testcases, bugs = columns(4)

with releases:
    metric(
        label="Releases",
        value=len(
            get_objects_by_filters(Release, {"project_shortname": current_project.split(':')[0]})
        ),
    )

with requirements:
    metric(
        label="Requirements",
        value=len(
            get_objects_by_filters(Requirement, {"project_shortname": current_project.split(':')[0]})
        ),
    )

with testcases:
    metric(
        label="Test cases",
        value=len(
            get_objects_by_filters(TestCase, {"project_shortname": current_project.split(':')[0]})
        ),
    )

with bugs:
    metric(
        label="Bugs",
        value=len(
            get_objects_by_filters(Bug, {"project_shortname": current_project.split(':')[0]})
        ),
    )
