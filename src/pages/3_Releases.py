from streamlit import button, columns, container, error, header, metric, session_state, sidebar, subheader, success, \
    write
from src.postgres_items_models import Bug, Project, Release, Status, Requirement, TestCase
from src.postgres_tasks_models import Task, TaskStatus
from src.postgres_sql_alchemy import create_database_object, edit_database_object, get_all_objects_by_type, \
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


def activate_release(release_shortname, refresh=False):
    """
    Set release state to Active if no other releases in project are active at the moment.

    :return: None.
    """
    if not refresh:
        activated_release = get_database_object(Release, release_shortname)
        activated_release["status"] = Status.Active.name
        edit_database_object(Release, activated_release["id"], activated_release)
        success(f"Release {activated_release['title']} is active now.")
    all_requirements = get_objects_by_filters(Requirement, {"target_release": release_shortname})
    all_test_cases = get_objects_by_filters(TestCase, {"target_release": release_shortname})
    all_bugs = get_objects_by_filters(Bug, {"target_release": release_shortname})
    for item in all_requirements + all_test_cases + all_bugs:
        if not item["children_task"]:
            object_type = shortname_prefix[item["shortname"].split("-")[0]]
            form_dict = {
                "title": f"Cover {item['shortname']}",
                "description": item["description"],
                "project_shortname": item["project_shortname"],
                "target_release": release_shortname,
                "status": TaskStatus.New.name
            }
            new_task = Task(**form_dict)
            item["children_task"] = create_database_object(new_task)
            edit_database_object(object_type, item["id"], item)
    if refresh:
        success("All tasks were updated.")


def finish_release(release_id):
    """
    Set release state to Implemented if number of tasks is equal to number of bugs, requirements and test cases.

    :return: None.
    """
    if len(all_tasks) != len(correlated_bugs) + len(correlated_requirements) + len(correlated_test_cases):
        error("Not all items are covered with tasks. Please use Refresh button.")
    else:
        form_dict = {"status": TaskStatus.Implemented.name}
        edit_database_object(Release, release_id, form_dict)
        success("Successfully finished release.")


header("Releases")
current_release = get_objects_by_filters(Release,
                                         {"project_shortname": session_state.current_project, "status": "Active"})
if current_release:
    current_release = current_release[-1]
    subheader(f"Current release: {current_release['title']}")

release_dataframe = []

parent_project = get_objects_by_filters(Project, {"title": session_state.current_project})[0]
all_releases = get_objects_by_filters(Release, {"project_shortname": session_state.current_project})

if len(all_releases) == 0:
    subheader("No releases available.")

for release in all_releases:
    correlated_requirements = get_objects_by_filters(Requirement, {"target_release": release["shortname"]})
    correlated_test_cases = get_objects_by_filters(TestCase, {"target_release": release["shortname"]})
    correlated_bugs = get_objects_by_filters(Bug, {"target_release": release["shortname"]})

    with container(border=True, ):
        subheader(f"{release['shortname']}: {release['title']}")
        req_col, tc_col, bug_col, status_col, button_col = columns([1, 1, 1, 2, 1])
        with req_col:
            metric("Requirements No.", len(correlated_requirements))
        with tc_col:
            metric("Test cases No.", len(correlated_test_cases))
        with bug_col:
            metric("Bugs No.", len(correlated_bugs))
        with status_col:
            metric("Status", release["status"])
        with button_col:
            if not current_release and release["status"] != "Implemented":
                button(label="Activate", key=f"{release['shortname']}_activate_button", on_click=activate_release,
                       args=(release["shortname"],))
            if current_release and current_release["shortname"] == release["shortname"]:
                all_tasks = get_objects_by_filters(Task, {"target_release": current_release["shortname"]})
                percentage_of_done = len([task for task in all_tasks if
                                          task["status"] == "Implemented"])/len(all_tasks)*100
                write(f"Completion: {round(percentage_of_done, 2)}%")
                if percentage_of_done == 100:
                    button(label="Finish", key=f"{release['shortname']}_finish_button", on_click=finish_release,
                           args=(release["id"],))
                button(label="Refresh", key=f"{release['shortname']}_refresh_button", on_click=activate_release,
                       args=(release["shortname"], True))
