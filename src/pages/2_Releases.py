from streamlit import button, columns, container, header, metric, sidebar, subheader
from postgres_items_models import Bug, Project, Release, Status, Requirement, TestCase
from postgres_tasks_models import Task, TaskStatus
from postgres_sql_alchemy import create_database_object, edit_database_object, get_all_objects_by_type, \
    get_database_object, get_objects_by_filters


shortname_prefix = {
    "proj": Project,
    "rls": Release,
    "req": Requirement,
    "tc": TestCase,
    "bug": Bug
}


def find_projects():
    """
    Get all available projects in list format.
    :return: List of Project database objects.
    """
    all_projects = get_all_objects_by_type(Project)
    return [f"{db_object['shortname']}: {db_object['title']}" for db_object in all_projects]


def activate_release(release_shortname):
    activated_release = get_database_object(Release, release_shortname)
    activated_release["status"] = Status.Active.name
    edit_database_object(Release, activated_release["id"], activated_release)
    all_requirements = get_objects_by_filters(Requirement, {"target_release": release_shortname})
    all_test_cases = get_objects_by_filters(TestCase, {"target_release": release_shortname})
    all_bugs = get_objects_by_filters(Bug, {"target_release": release_shortname})
    for item in all_requirements + all_test_cases + all_bugs:
        if not item["children_task"]:
            object_type = shortname_prefix[item["shortname"].split("-")[0]]
            form_dict = {
                "title": f"Cover {item['shortname']}",
                "description": item["description"],
                "status": TaskStatus.New.name
            }
            new_task = Task(**form_dict)
            item["children_task"] = create_database_object(new_task)
            edit_database_object(object_type, item["id"], item)


current_project = sidebar.selectbox(
    label="current_project",
    key="current_project",
    options=find_projects(),
    index=0,
    placeholder="Select project...",
    label_visibility="collapsed",
)

header("Releases")
all_releases = get_objects_by_filters(Release, {"project_shortname": current_project.split(':')[0]})

release_dataframe = []

for release in all_releases:
    correlated_requirements = get_objects_by_filters(Requirement, {"target_release": release["shortname"]})
    correlated_test_cases = get_objects_by_filters(TestCase, {"target_release": release["shortname"]})
    correlated_bugs = get_objects_by_filters(Bug, {"target_release": release["shortname"]})

    with container(border=True, ):
        subheader(f"{release['shortname']}: {release['title']}")
        req_col, tc_col, bug_col, status_col, button_col = columns(5)
        with req_col:
            metric("Requirements No.", len(correlated_requirements))
        with tc_col:
            metric("Test cases No.", len(correlated_test_cases))
        with bug_col:
            metric("Bugs No.", len(correlated_bugs))
        with status_col:
            metric("Status", release["status"])
        with button_col:
            button(label="Activate", key=f"{release['shortname']}_button", on_click=activate_release,
                   args=(release["shortname"],))
