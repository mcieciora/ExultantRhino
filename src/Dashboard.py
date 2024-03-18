from requests import get
from streamlit import columns, header, sidebar, metric


def find_projects():
    all_projects = get("http://api:8101/get_objects/project")
    print(all_projects)
    return [f"{db_object['shortname']}: {db_object['title']}" for db_object in all_projects.json()]


current_project = sidebar.selectbox(label="current_project",
                                    key="current_project",
                                    options=find_projects(),
                                    index=0,
                                    placeholder="Select project...",
                                    label_visibility="collapsed")


header("Dashboard")
releases, requirements, testcases, bugs = columns(4)

with releases:
    metric(label="Releases",
           value=len(get(f"http://api:8101/get_objects/release?project_id={current_project.split(':')[0]}").json()))

with requirements:
    metric(label="Requirements",
           value=len(get(f"http://api:8101/get_objects/requirement?project_id="
                         f"{current_project.split(':')[0]}").json()))

with testcases:
    metric(label="Test cases",
           value=len(get(f"http://api:8101/get_objects/testcase?project_id={current_project.split(':')[0]}").json()))

with bugs:
    metric(label="Bugs",
           value=len(get(f"http://api:8101/get_objects/bug?project_id={current_project.split(':')[0]}").json()))
