from pandas import DataFrame
from streamlit import column_config, dataframe, header, sidebar
from src.postgres_items_models import Project
from src.postgres_tasks_models import Task
from src.postgres_sql_alchemy import get_all_objects_by_type


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

header("Tasks")
all_objects = get_all_objects_by_type(Task)

df = DataFrame(all_objects)

dataframe(all_objects,
          column_config={
              "id": "ID",
              "shortname": "Shortname",
              "title": "Title",
              "description": "Description",
              "status": "Status",
              "project_shortname": "Project",
              "target_release": "Release",
              "parent": "Parent",
              "url": column_config.LinkColumn("Edit URL", display_text="Edit")
          },
          column_order=("id", "shortname", "title", "description", "status", "project_shortname", "parent",
                        "target_release", "url"),
          hide_index=True
          )
