from streamlit import columns, container, header, markdown, metric, session_state, sidebar, subheader
from src.postgres_items_models import Project, Result
from src.postgres_sql_alchemy import get_all_objects_by_type, get_objects_by_filters


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

header("Results")
all_objects = get_objects_by_filters(Result, {"project_shortname": session_state.current_project})

if len(all_objects) == 0:
    subheader("No results uploaded.")

for item in all_objects:
    all_tests = sum([item["passed"], item["failed"], item["skipped"]])
    try:
        pass_rate = item["passed"]/all_tests
        rounded_pass_rate = round(pass_rate, 2)
        pass_rate = rounded_pass_rate*100
    except ZeroDivisionError:
        pass_rate = 0.0
    with container(border=True, ):
        title_column, pass_rate_column, view_column = columns([4, 2, 1])
        with title_column:
            markdown(item['title'])
        with pass_rate_column:
            metric(label="Pass rate", value=f"{pass_rate}%")
        with view_column:
            markdown(f"[View]({item['build_url']})")
