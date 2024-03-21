from requests import get
from streamlit import expander, header, sidebar, write


def find_projects():
    all_projects = get("http://api:8101/get_objects/project")
    print(all_projects)
    return [
        f"{db_object['shortname']}: {db_object['title']}"
        for db_object in all_projects.json()
    ]


current_project = sidebar.selectbox(
    label="current_project",
    key="current_project",
    options=find_projects(),
    index=0,
    placeholder="Select project...",
    label_visibility="collapsed",
)

header("Backlog")
all_releases = get(
    f"http://api:8101/get_objects/release?project_id={current_project.split(':')[0]}"
)

for release in all_releases.json():
    all_reqs = get(
        f"http://api:8101/get_objects/requirement?parent={release['shortname']}"
    ).json()
    with expander(f"    Release: {release['title']}"):
        for req in all_reqs:
            write(req["title"])
