from requests import get
from streamlit import header, sidebar, write


def find_projects():
    """
    Get all available projects in list format.
    :return: List of Project database objects.
    """
    all_projects = get("http://localhost:8101/get_objects/project", timeout=5)
    return [db_object['title'] for db_object in all_projects.json()]


current_project = sidebar.selectbox(
    label="current_project",
    key="current_project",
    options=find_projects(),
    index=0,
    placeholder="Select project...",
    label_visibility="collapsed",
)

header("Releases")
all_releases = get(f"http://localhost:8101/get_objects/release?project_id={current_project.split(':')[0]}")

for release in all_releases.json():
    all_reqs = get(f"http://localhost:8101/get_objects/requirement?parent={release['parent'].split(':')[0]}").json()
    write(f"Release: {release['title']}")
    for req in all_reqs:
        write(f":{req['title']}")
        all_tcs = get(f"http://localhost:8101/get_objects/testcase?parent={req['parent'].split(':')[0]}").json()
        for tc in all_tcs:
            write(f"::{tc['title']}")
