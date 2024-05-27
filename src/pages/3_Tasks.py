from pandas import DataFrame
from streamlit import button, column_config, dataframe, header, selectbox, sidebar, success, text_area, text_input, \
    query_params
from src.postgres_items_models import Project
from src.postgres_tasks_models import Task, TaskStatus
from src.postgres_sql_alchemy import edit_database_object, get_all_objects_by_type, get_objects_by_filters


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


def update_task(task_id):
    edit_database_object(Task, task_id, form_dict)


parameters = query_params
if parameters:
    task = get_objects_by_filters(Task, {"shortname": parameters["item"]})[0]
    statuses = [status.name for status in TaskStatus]
    status_index = statuses.index(task["status"])
    form_dict = {
        "title": text_input("Title", key="task_title", value=task["title"]),
        "description": text_area("Description", key="task_description", value=task["description"]),
        "status": selectbox("Status", key="task_status", options=statuses, index=status_index),
    }

    if button(label="Update", key="task_update_button", on_click=update_task, args=(task["id"],)):
        success(f"Updated {task['title']}")
else:
    header("Tasks")
    all_objects = get_all_objects_by_type(Task)

    for item in all_objects:
        item["url"] = f"http://localhost:8501/Tasks?item={item['shortname']}"

    df = DataFrame(all_objects)

    dataframe(all_objects,
              column_config={
                  "shortname": "Shortname",
                  "title": "Title",
                  "description": "Description",
                  "status": "Status",
                  "parent": "Parent",
                  "url": column_config.LinkColumn("View URL", display_text="View")
              },
              column_order=("shortname", "title", "description", "status", "url"),
              hide_index=True
              )
