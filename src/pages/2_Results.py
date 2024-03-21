from requests import get
from streamlit import header, sidebar


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

header("Active release")
