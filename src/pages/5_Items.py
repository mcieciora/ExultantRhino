from os import environ
from streamlit import columns, container, header, markdown, selectbox, session_state, sidebar
from src.postgres_items_models import Project, Release, Requirement, TestCase, Bug
from src.postgres_sql_alchemy import get_all_objects_with_filters, get_all_objects_by_type, get_objects_by_filters


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

header_column, select_box_column = columns(2)
with header_column:
    header("Items")
with select_box_column:
    selected_release = selectbox(
        label="Filter by release",
        label_visibility="collapsed",
        key="filtered_release",
        options=[f"{db_object['title']}" for db_object in
                 get_objects_by_filters(Release, {"project_shortname": session_state.current_project})],
        placeholder="Filter by release..."
    )
all_objects = [get_objects_by_filters(Project, {"title": session_state.current_project})[0]]
if selected_release:
    target_release = get_objects_by_filters(Release, {"title": selected_release})[0]
    all_objects.append(target_release)
    all_objects.extend(get_all_objects_with_filters([Requirement, TestCase, Bug],
                                                    {"project_shortname": session_state.current_project,
                                                     "target_release": target_release["shortname"]}))
else:
    all_objects.extend(get_all_objects_with_filters([Release, Requirement, TestCase, Bug],
                                                    {"project_shortname": session_state.current_project}))

for item in all_objects:
    item["url"] = f"http://{environ['APP_HOST']}:8501/+Create?item={item['shortname']}"
    with container(border=True, ):
        title_column, view_column = columns([6, 1])
        with title_column:
            markdown(f"{item['title']}")
        with view_column:
            markdown(f"[View]({item['url']})")
