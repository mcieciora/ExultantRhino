from streamlit import button, header, selectbox, sidebar, success, text_area, text_input, query_params, warning, write
from streamlit_searchbox import st_searchbox
from postgres_items_models import Bug, Project, Release, Requirement, TestCase, Status
from postgres_sql_alchemy import create_database_object, edit_database_object, get_all_objects_by_type, \
    get_all_objects_with_filters, get_database_object, get_objects_by_filters


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
    "Bug": Bug,
}

form_dict = {}

parameters = query_params
if parameters:
    header("Edit an item")
    item_prefix = parameters["item"].split("-")[0]
    item_object_type = shortname_prefix[item_prefix]
    item = get_database_object(item_object_type, parameters["item"])
else:
    header("Create new item")


def get_parent_target_release(parent):
    parent_object_type = get_parent_object_type(object_type)
    for db_object in get_all_objects_by_type(parent_object_type):
        if db_object["shortname"] == parent:
            return db_object["target_release"]


def get_parent_object_type(input_type):
    parent_objects_map = {
        Release: Project,
        Requirement: Release,
        TestCase: Requirement,
        Bug: TestCase,
    }
    return parent_objects_map[object_type_db_object_map[input_type]]


def find_available_parents(search_term):
    parent_object_type = get_parent_object_type(object_type)
    available_parents = get_objects_by_filters(parent_object_type, {"project_shortname": current_project.split(":")[0]})
    if search_term == "":
        return [
            f"{db_object['shortname']}: {db_object['title']}"
            for db_object in available_parents
        ]
    else:
        return [
            f"{db_object['shortname']}: {db_object['title']}"
            for db_object in available_parents
            if search_term in db_object["shortname"] or search_term in db_object["title"]
        ]


def find_projects(search_term):
    all_projects = get_all_objects_by_type(Project)
    return [
        f"{db_object['shortname']}: {db_object['title']}"
        for db_object in all_projects
        if search_term in db_object["shortname"] or search_term in db_object["title"]
    ]


def verify_form():
    for key, value in form_dict.items():
        if value in ["", None]:
            warning("All field must be filled")
            return False
    if "project_shortname" in form_dict:
        form_dict["project_shortname"] = form_dict["project_shortname"].split(":")[0]
    if "parent" in form_dict:
        form_dict["parent"] = form_dict["parent"].split(":")[0]
    if object_type == "Release":
        form_dict["parent"] = form_dict["project_shortname"]
        form_dict["status"] = Status.New.name
    if object_type == "Requirement":
        form_dict["target_release"] = form_dict["parent"]
    if object_type in ["Test case", "Bug"]:
        parent_shortname = form_dict["parent"]
        form_dict["target_release"] = get_parent_target_release(parent_shortname)
    return True


def changes_detected():
    if ret_dict := {key: value for key, value in form_dict.items() if value not in ["", None] and item[key] != value}:
        return ret_dict
    else:
        warning("Nothing was changed.")
        return False


object_type = selectbox(
    label="Select object type",
    key="object_type",
    options=("Project", "Release", "Requirement", "Test case", "Bug"),
    index=["Project", "Release", "Requirement", "Test case", "Bug"].index(item_object_type.__name__)
    if parameters else None,
    placeholder="Select card type...",
    disabled=True if parameters else False
)

if object_type:
    form_map = {
        "title": {
            "applicable": ["Project", "Release", "Requirement", "Test case", "Bug"],
            "streamlit_function": text_input,
            "default_value_field": "value",
            "default_value": f"Insert {object_type.lower()} title",
            "args": {
                "label": "Title",
                "key": "title",
            }
        },
        "description": {
            "applicable": ["Project", "Release", "Requirement", "Test case", "Bug"],
            "streamlit_function": text_area,
            "default_value_field": "value",
            "default_value": f"Insert {object_type.lower()} description",
            "args": {
                "label": "Description",
                "key": "description"
            }
        },
        "project_shortname": {
            "applicable": ["Release", "Requirement", "Test case", "Bug"],
            "streamlit_function": text_input,
            "default_value_field": "value",
            "default_value": current_project,
            "args": {
                "label": "Parent project",
                "disabled": True,
                "key": "parent_project_search_box"
            }
        },
        "parent": {
            "applicable": ["Requirement", "Test case", "Bug"],
            "streamlit_function": st_searchbox,
            "default_value_field": "placeholder",
            "default_value": "Search ...",
            "args": {
                "label": "Parent item",
                "search_function": find_available_parents,
                "key": "parent_item_search_box"
            }
        },
    }

    for form_key, form_item in form_map.items():
        if object_type in form_item["applicable"]:
            form_item["args"][form_item["default_value_field"]] = item[form_key] if parameters else form_item["default_value"]
            form_dict[form_key] = form_item["streamlit_function"](**form_item["args"])

    if parameters:
        if button(label="Update"):
            if verify_form() and (item_edited := changes_detected()):
                edit_database_object(object_type_db_object_map[object_type], item["id"], item_edited)

                #     if object_type is Release:
                #         form_dict["parent"] = form_dict["project_shortname"]
                #         all_child_objects = get_all_objects_with_filters([Requirement, TestCase, Bug],
                #                                                          {"parent": form_dict["shortname"]})
                #         for db_object in all_child_objects:
                #             if "rls" in db_object["shortname"]:
                #                 edit_database_object(Requirement, db_object["id"], form_dict)
                #     edit_database_object(object_type, database_object["id"], form_dict)

                # active to edit
                # project all
                # release: project as searchbox; remove parent
                # requirement: release as searchbox; remove parent
                # tc and bug: parent

                # TODO add tc and bug edition later
                # project title and desc changes
                # if edited release column: project then update release parent and all items parent and target_release columns equal to release shortname
                # if edited req column: release then update parent and all items that equal req parent and all their children to release shortname
                success(f"{item['shortname']}: {item['title']} was updated.")
        if button(label="Delete"):
            warning("Deletion to be implemented.")
    elif button(label="Submit"):
        if verify_form():
            new_object = object_type_db_object_map[object_type](**form_dict)
            new_object_id = create_database_object(new_object)
            success(f"Created {new_object_id}")
        else:
            warning("All fields are required.")
