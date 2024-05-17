from streamlit import button, header, selectbox, success, text_area, text_input, query_params, write
from streamlit_searchbox import st_searchbox
from postgres_items_models import Bug, Project, Release, Requirement, TestCase, Status
from postgres_sql_alchemy import create_database_object, edit_database_object, get_all_objects_by_type, \
    get_all_objects_with_filters, get_database_object, get_objects_by_filters


shortname_prefix = {
    "proj": Project,
    "rls": Release,
    "req": Requirement,
    "tc": TestCase,
    "bug": Bug
}


def get_parent_object_type(input_type):
    database_object_map = {
        "Release": Release,
        "Requirement": Requirement,
        "Test case": TestCase,
        "Bug": Bug,
    }
    parent_objects_map = {
        Release: Project,
        Requirement: Release,
        TestCase: Requirement,
        Bug: TestCase,
    }
    return parent_objects_map[database_object_map[input_type]]


def get_parent_target_release(parent):
    parent_object_type = get_parent_object_type(object_type)
    for db_object in get_all_objects_by_type(parent_object_type):
        if db_object["shortname"] == parent:
            return db_object["target_release"]


def find_available_parents(search_term):
    parent_object_type = get_parent_object_type(object_type)
    available_parents = get_all_objects_by_type(parent_object_type)
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


parameters = query_params
if parameters:
    header("Edit an item")
    standard_prefix = parameters["item"].split("-")[0]
    object_type = shortname_prefix[standard_prefix]
    database_object = get_database_object(object_type, parameters["item"])
    write(parameters)
    form_dict = {}
    for key, value in database_object.items():
        if all([object_type is Release or object_type is Requirement, key in ["parent"]]):
            continue
        if object_type is Release and key == "project_shortname":
            form_dict["project_shortname"] = st_searchbox(
                find_projects,
                placeholder=value,
                label="Parent project",
                key="parent_project_search_box"
            )
        else:
            form_dict[key] = text_input(
                label=key.replace("_", " ").capitalize(), key=f"parameter_{key}", disabled=key in ["id", "shortname"],
                value=value
            )
    if button(label="Update"):
        if object_type is Release:
            form_dict["parent"] = form_dict["project_shortname"]
            all_child_objects = get_all_objects_with_filters([Requirement, TestCase, Bug], {"parent": form_dict["shortname"]})
            for db_object in all_child_objects:
                if "rls" in db_object["shortname"]:
                    edit_database_object(Requirement, db_object["id"], form_dict)
        edit_database_object(object_type, database_object["id"], form_dict)
else:
    header("Create new item")
    object_type = selectbox(
        label="Select object type",
        key="object_type",
        options=("Project", "Release", "Requirement", "Test case", "Bug"),
        index=None,
        placeholder="Select card type...",
    )

    form_dict = {}

    if object_type:
        form_dict["title"] = text_input(
            label="Title", key="title", placeholder=f"Insert {object_type.lower()} title"
        )

        if object_type in ["Release", "Requirement", "Test case", "Bug"]:
            form_dict["project_shortname"] = st_searchbox(
                find_projects,
                label="Parent project",
                key="parent_project_search_box",
                placeholder="Search ...",
            )

        form_dict["description"] = text_area(
            label="Description",
            key="description",
            placeholder=f"Insert {object_type.lower()} description",
        )

        if object_type in ["Requirement", "Test case", "Bug"]:
            form_dict["parent"] = st_searchbox(
                find_available_parents,
                label="Parent item",
                key="parent_item_search_box",
                placeholder="Search ...",
            )

        if button(label="Submit"):
            object_type_db_object_map = {
                "Project": Project,
                "Release": Release,
                "Requirement": Requirement,
                "Test case": TestCase,
                "Bug": Bug,
            }
            if object_type in ["Release", "Requirement", "Test case", "Bug"]:
                form_dict["project_shortname"] = form_dict["project_shortname"].split(":")[0]
            if object_type == "Release":
                form_dict["parent"] = form_dict["project_shortname"]
                form_dict["status"] = Status.New.name
            if object_type not in ["Project", "Release"]:
                form_dict["parent"] = form_dict["parent"].split(":")[0]
            if object_type == "Requirement":
                form_dict["target_release"] = form_dict["parent"]
            if object_type in ["Test case", "Bug"]:
                parent_shortname = form_dict["parent"]
                form_dict["target_release"] = get_parent_target_release(parent_shortname)
            new_object = object_type_db_object_map[object_type](**form_dict)
            new_object_id = create_database_object(new_object)
            success(f"Created {new_object_id}")
