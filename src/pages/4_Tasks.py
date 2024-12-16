from os import environ
from streamlit import button, columns, container, header, markdown, selectbox, session_state, sidebar, subheader, \
    success, text_area, text_input, warning, query_params
from src.postgres_items_models import Project, Release
from src.postgres_tasks_models import Task, TaskStatus
from src.postgres_sql_alchemy import edit_database_object, get_all_objects_by_type, get_objects_by_filters


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


def update_task(form_dict, task_id):
    """
    Update task with form_dict data by given id.

    :return: None.
    """
    edit_database_object(Task, task_id, form_dict)


def page(edit_page):
    """
    Page function.

    :return: None
    """
    if edit_page:
        statuses = [status.name for status in TaskStatus]
        status_index = statuses.index(task["status"])
        form_dict = {
            "title": text_input("Title", key="task_title", value=task["title"]),
            "description": text_area("Description", key="task_description", value=task["description"]),
            "status": selectbox("Status", key="task_status", options=statuses, index=status_index),
        }

        if button(label="Update", key="task_update_button", on_click=update_task, args=(form_dict, task["id"],)):
            success(f"Updated {task['title']}")
    else:
        header_column, select_box_column = columns(2)
        with header_column:
            header("Tasks")
        with select_box_column:
            selected_task_status = selectbox(
                label="Filter by status",
                label_visibility="collapsed",
                key="filtered_statuses",
                options=["All"]+[status.name for status in TaskStatus],
                placeholder="Filter by release..."
            )
        try:
            target_release = get_objects_by_filters(Release, {"status": "Active"})[0]
            if selected_task_status == "All":
                all_objects = get_objects_by_filters(Task, {"project_shortname": session_state.current_project,
                                                            "target_release": target_release["shortname"]})
            else:
                all_objects = get_objects_by_filters(Task, {"project_shortname": session_state.current_project,
                                                            "target_release": target_release["shortname"],
                                                            "status": selected_task_status})

            for item in all_objects:
                item["url"] = f"http://{environ['APX_HOST']}:8501/Tasks?item={item['shortname']}"
                with container(border=True, ):
                    title_column, status_column, view_column = columns([5, 2, 1])
                    with title_column:
                        markdown(item['title'])
                    with status_column:
                        markdown(item["status"])
                    with view_column:
                        markdown(f"[View]({item['url']})")
        except (IndexError, TypeError):
            subheader("No active release.")


def not_found():
    """
    Not found page.

    :return: None
    """
    warning("Task not found")


parameters = query_params
if parameters:
    header("Edit task")
    try:
        task = get_objects_by_filters(Task, {"shortname": parameters["item"]})[0]
        page(edit_page=True)
    except IndexError:
        not_found()
else:
    page(edit_page=False)
