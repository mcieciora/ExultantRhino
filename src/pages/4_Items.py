from streamlit import column_config, dataframe, header, sidebar
from pandas import DataFrame
from postgres_items_models import Project, Release, Requirement, TestCase, Bug
from postgres_sql_alchemy import get_database_object, get_all_objects_with_filters, get_all_objects_by_type, create_database_object


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

header("Items")
all_objects = [get_database_object(Project, current_project.split(":")[0])]
all_objects.extend(get_all_objects_with_filters([Release, Requirement, TestCase, Bug], {"project_shortname": current_project.split(":")[0]}))
for item in all_objects:
    item["url"] = f"http://localhost:8501/+Create?item={item['shortname']}"

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
              "children_task": "Task",
              "url": column_config.LinkColumn("Edit URL", display_text="Edit")
          },
          column_order=("id", "shortname", "title", "description", "status", "project_shortname", "parent",
                        "children_task", "target_release", "url"),
          hide_index=True
          )
