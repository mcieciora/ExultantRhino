from os import environ
from streamlit import column_config, dataframe, header, session_state, sidebar
from pandas import DataFrame
from src.postgres_items_models import Project, Release, Requirement, TestCase, Bug
from src.postgres_sql_alchemy import get_all_objects_with_filters, get_all_objects_by_type, get_objects_by_filters


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

header("Items")
all_objects = [get_objects_by_filters(Project, {"title": current_project})[0]]
all_objects.extend(get_all_objects_with_filters([Release, Requirement, TestCase, Bug],
                                                {"project_shortname": current_project}))
for item in all_objects:
    item["url"] = f"http://{environ['API_HOST']}:8501/+Create?item={item['shortname']}"

df = DataFrame(all_objects)

dataframe(all_objects,
          column_config={
              "shortname": "Shortname",
              "title": "Title",
              "description": "Description",
              "status": "Status",
              "project_shortname": "Project",
              "target_release": "Release",
              "parent": "Parent",
              "children_task": "Task",
              "url": column_config.LinkColumn("View URL", display_text="View")
          },
          column_order=("shortname", "title", "description", "status", "project_shortname", "parent",
                        "children_task", "target_release", "url"),
          hide_index=True
          )
