from requests import get
from streamlit import button, error, header, selectbox, success, text_area, text_input
from streamlit_searchbox import st_searchbox
from postgres_models import Bug, Project, Release, Requirement, TestCase


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


def find_parent(search_term):
    parent_object = get_parent_object_type(object_type)
    api_call_result = get(
        f"http://localhost:8101/get_objects/{parent_object.__name__.lower()}"
    )
    print(api_call_result)
    return [
        db_object['shortname']
        for db_object in api_call_result.json()
        if search_term in db_object["shortname"] or search_term in db_object["title"]
    ]


def find_projects(search_term):
    all_projects = get("http://localhost:8101/get_objects/project")
    print(all_projects)
    return [
        f"{db_object['shortname']}: {db_object['title']}"
        for db_object in all_projects.json()
        if search_term in db_object["shortname"] or search_term in db_object["title"]
    ]


header("Create new card")
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
        form_dict["project_id"] = st_searchbox(
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
            find_parent,
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
        new_object = object_type_db_object_map[object_type](**form_dict)
        return_value = get(
            f"http://localhost:8101/insert_object/{object_type.replace(' ', '').lower()}",
            params=form_dict,
        )
        if return_value.status_code == 200:
            success(return_value.text)
        else:
            error(return_value.text)
