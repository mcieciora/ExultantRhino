from os import environ
from time import sleep
from streamlit import button, columns, header, markdown, selectbox, session_state, sidebar, success, text_area, \
    text_input, query_params, warning, switch_page
from src.postgres_items_models import Bug, Project, Release, Requirement, TestCase, Status
from src.postgres_tasks_models import Task
from src.postgres_sql_alchemy import create_database_object, delete_database_object, edit_database_object, \
    get_all_objects_by_type, get_database_object, get_downstream_items, get_objects_by_filters


PAGE_REDIRECT_WAIT = 1.0

shortname_prefix = {
    "proj": Project,
    "rls": Release,
    "req": Requirement,
    "tc": TestCase,
    "bug": Bug
}

object_type_db_object_map = {
    "Project": Project,
    "Release": Release,
    "Requirement": Requirement,
    "Test case": TestCase,
    "Bug": Bug
}

form_dict = {}


def find_projects():
    """
    Get all available projects in list format.

    :return: List of Project database objects.
    """
    return [f"{db_object['title']}" for db_object in get_all_objects_by_type(Project)]


all_projects = find_projects()
disabled = False
if query_params:
    try:
        item_prefix = query_params["item"].split("-")[0]
        item_object_type = shortname_prefix[item_prefix]
        item = get_database_object(item_object_type, query_params["item"])
        index = all_projects.index(item["project_shortname"])
        disabled = True
    except KeyError:
        index = 0
elif "current_project" in session_state:
    index = all_projects.index(session_state["current_project"])
else:
    index = 0
session_state.current_project = sidebar.selectbox(
    label="current_project_select_box",
    key="current_project_select_box",
    options=all_projects,
    index=index,
    placeholder="Select project...",
    label_visibility="collapsed",
    disabled=disabled
)


def get_parent_target_release(object_type, parent):
    """
    Get target release value of parent object.

    :return: Target release value.
    """
    parent_object_type = get_parent_object_type(object_type)
    for db_object in get_all_objects_by_type(parent_object_type):
        if db_object["shortname"] == parent:
            return db_object["target_release"]


def get_parent_object_type(input_type):
    """
    Get parent object type using declared mapping.

    :return: Object type.
    """
    parent_objects_map = {
        Release: Project,
        Requirement: Release,
        TestCase: Requirement,
        Bug: TestCase,
    }
    return parent_objects_map[object_type_db_object_map[input_type]]


def find_available_parents(object_type, return_pretty=False):
    """
    Find available parent of an object, that are created in currently chosen project.

    :return: List of database shortnames.
    """
    parent_object_type = get_parent_object_type(object_type)
    query = get_objects_by_filters(parent_object_type, {"project_shortname": session_state.current_project})
    if return_pretty:
        return [f"{db_object['shortname']}: {db_object['title']}" for db_object in query]
    else:
        return [db_object["shortname"] for db_object in query]


def verify_form(object_type, edit=False):
    """
    Form verification function.

    :return: True or False depending on verification result.
    """
    if object_type == "Project" and edit and form_dict["title"] != item["title"]:
        warning("Project title cannot be edited.")
        return False
    for key, value in form_dict.items():
        if value in ["", None]:
            warning("All field must be filled")
            return False
    if "project_shortname" in form_dict:
        form_dict["project_shortname"] = form_dict["project_shortname"]
    if "parent" in form_dict:
        form_dict["parent"] = form_dict["parent"].split(":")[0]
    if object_type == "Release":
        form_dict["parent"] = form_dict["project_shortname"]
        form_dict["status"] = Status.New.name
    if object_type == "Requirement":
        form_dict["target_release"] = form_dict["parent"]
    if object_type in ["Test case", "Bug"]:
        parent_shortname = form_dict["parent"]
        form_dict["target_release"] = get_parent_target_release(object_type, parent_shortname)
    return True


def changes_detected():
    """
    Verify if any changes were made to current form values.

    :return: True or False depending on verification result.
    """
    if ret_dict := {key: value for key, value in form_dict.items() if value not in ["", None] and item[key] != value}:
        return ret_dict
    else:
        warning("Nothing was changed.")
        return False


def delete_item(object_type):
    """
    Form object deletion.

    :return: None
    """
    tasks_count = 0
    parent_item = get_database_object(object_type_db_object_map[object_type], item["shortname"])
    downstream_items = get_downstream_items(object_type_db_object_map[object_type], item["shortname"])
    downstream_items.append(parent_item)
    for downstream_item in downstream_items:
        if "children_task" in downstream_item and downstream_item["children_task"]:
            task = get_database_object(Task, downstream_item["children_task"])
            delete_database_object(Task, task["id"])
            tasks_count += 1
        delete_database_object(shortname_prefix[downstream_item["shortname"].split("-")[0]], downstream_item["id"])
    success(f"Deleted {item['title']}, {len(downstream_items)} related items and {tasks_count} tasks")
    sleep(PAGE_REDIRECT_WAIT)


def delete_project():
    """
    Form project deletion.

    :return: None
    """
    tasks_count = 0
    for downstream_item in (downstream_items := get_downstream_items(Project, item["title"])):
        if "children_task" in downstream_item and downstream_item["children_task"]:
            task = get_database_object(Task, downstream_item["children_task"])
            delete_database_object(Task, task["id"])
            tasks_count += 1
        delete_database_object(shortname_prefix[downstream_item["shortname"].split("-")[0]], downstream_item["id"])
    delete_database_object(shortname_prefix[item["shortname"].split("-")[0]], item["id"])
    success(f"Deleted {item['title']}, {len(downstream_items)} related items and {tasks_count} tasks")
    sleep(PAGE_REDIRECT_WAIT)


def edit_object(object_type, changes_dict):
    """
    Form object edition.

    :return: None
    """
    if "parent" in changes_dict:
        parent_item = get_objects_by_filters(get_parent_object_type(object_type),
                                             {"shortname": form_dict["parent"]})[-1]
        if object_type_db_object_map[object_type] is Requirement and \
                parent_item["shortname"] != item["target_release"]:
            for downstream_item in get_downstream_items(object_type_db_object_map[object_type],
                                                        item["shortname"]):
                downstream_item_type = shortname_prefix[downstream_item["shortname"].split("-")[0]]
                edit_database_object(downstream_item_type, downstream_item["id"],
                                     {"target_release": form_dict["parent"]})
        elif object_type_db_object_map[object_type] in [TestCase, Bug] and \
                parent_item["target_release"] != item["target_release"]:
            for downstream_item in get_downstream_items(object_type_db_object_map[object_type],
                                                        item["shortname"]):
                downstream_item_type = shortname_prefix[downstream_item["shortname"].split("-")[0]]
                edit_database_object(downstream_item_type, downstream_item["id"],
                                     {"target_release": parent_item["target_release"]})
    edit_database_object(object_type_db_object_map[object_type], item["id"], form_dict)
    success(f"{item['shortname']}: {item['title']} was updated.")
    sleep(PAGE_REDIRECT_WAIT)


def generate_streamlit_form(object_type, form_map, parent_item_options):
    """
    Generate form dict for streamlit UI form.

    :return: None
    """
    for form_key, form_item in form_map.items():
        if object_type in form_item["applicable"]:
            if parameters:
                if form_key == "parent":
                    form_item["args"][form_item["parametrized_value_field"]] = \
                        [x.split(":")[0] for x in parent_item_options].index(item[form_key])
                else:
                    form_item["args"][form_item["parametrized_value_field"]] = item[form_key]
            else:
                form_item["args"][form_item["default_value_field"]] = form_item["default_value"]
            form_dict[form_key] = form_item["streamlit_function"](**form_item["args"])


def submit(object_type):
    """
    On click wrapper that clears form fields.

    :return: None
    """
    if verify_form(object_type):
        new_object = object_type_db_object_map[object_type](**form_dict)
        if new_object_id := create_database_object(new_object):
            success(f"Created {new_object_id}")
            for key in list(session_state.keys()):
                del session_state[key]
        else:
            warning(f"Project with title: {new_object.title} already exists.")


def page():
    """
    Page function.

    :return: None
    """
    object_type = selectbox(
        label="Select object type",
        key="object_type",
        options=("Project", "Release", "Requirement", "Test case", "Bug"),
        index=["Project", "Release", "Requirement", "TestCase", "Bug"].index(item_object_type.__name__)
        if parameters else None,
        placeholder="Select card type...",
        disabled=True if parameters else False
    )

    if object_type:
        parent_item_options = find_available_parents(object_type, return_pretty=True) if object_type in \
                                                                            ["Requirement", "Test case", "Bug"] else []

        form_map = {
            "title": {
                "applicable": ["Project", "Release", "Requirement", "Test case", "Bug"],
                "streamlit_function": text_input,
                "parametrized_value_field": "value",
                "default_value_field": "placeholder",
                "default_value": f"Insert {object_type.lower()} title",
                "args": {
                    "label": "Title",
                    "key": "title",
                }
            },
            "description": {
                "applicable": ["Project", "Release", "Requirement", "Test case", "Bug"],
                "streamlit_function": text_area,
                "parametrized_value_field": "value",
                "default_value_field": "placeholder",
                "default_value": f"Insert {object_type.lower()} description",
                "args": {
                    "label": "Description",
                    "key": "description"
                }
            },
            "project_shortname": {
                "applicable": ["Release", "Requirement", "Test case", "Bug"],
                "streamlit_function": text_input,
                "parametrized_value_field": "value",
                "default_value_field": "value",
                "default_value": session_state.current_project,
                "args": {
                    "label": "Parent project",
                    "disabled": True,
                    "key": "parent_project_text_input"
                }
            },
            "parent": {
                "applicable": ["Requirement", "Test case", "Bug"],
                "streamlit_function": selectbox,
                "parametrized_value_field": "index",
                "default_value_field": "placeholder",
                "default_value": "Search for parent item...",
                "args": {
                    "label": "Parent item",
                    "options": parent_item_options,
                    "key": "parent_item_select_box",
                    "index": None
                }
            }
        }

        generate_streamlit_form(object_type, form_map, parent_item_options)

        if parameters:
            if object_type in ["Requirement", "Test case", "Bug"] and item["children_task"]:
                related_task_url = f"http://{environ['APP_HOST']}:8501/Tasks?item={item['children_task']}"
                markdown(f"Related task: [{item['children_task']}]({related_task_url})")
            update_button_col, delete_button_col, nan_col = columns([1, 1, 5])
            with update_button_col:
                if button(label="Update"):
                    if verify_form(object_type, edit=True) and (changes_dict := changes_detected()):
                        edit_object(object_type, changes_dict)
                        switch_page("pages/5_Items.py")
            with delete_button_col:
                if button(label="Delete"):
                    if object_type == "Project":
                        if item["title"] == "DEFAULT":
                            warning("DEFAULT project cannot be deleted.")
                            return False
                        else:
                            delete_project()
                            session_state["current_project"] = "DEFAULT"
                            switch_page("pages/5_Items.py")
                    else:
                        delete_item(object_type)
                        switch_page("pages/5_Items.py")
        elif button(label="Submit", on_click=submit, args=(object_type,)):
            pass


def not_found():
    """
    Not found page.

    :return: None
    """
    warning("Item not found")


parameters = query_params
if parameters:
    header("Edit an item")
    item_prefix = parameters["item"].split("-")[0]
    item_object_type = shortname_prefix[item_prefix]
    item = get_database_object(item_object_type, parameters["item"])
    if item:
        page()
    else:
        not_found()
else:
    header("Create new item")
    page()
