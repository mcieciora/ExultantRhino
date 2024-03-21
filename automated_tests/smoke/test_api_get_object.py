from requests import get
from pytest import mark


@mark.smoke
def test__smoke__api__get_object__project(one_object_of_type_database_fixture):
    api_call_url = "http://exultant_rhino_api:8101/get_object/project/proj-0"
    api_call = get(api_call_url, timeout=5)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert database_object["title"] == "new project", f"title value equals {database_object['title']}"
    assert database_object["description"] == "description of new project", f"description value equals " \
                                                                           f"{database_object['description']}"


@mark.smoke
def test__smoke__api__get_object__bug(one_object_of_type_database_fixture):
    api_call_url = "http://exultant_rhino_api:8101/get_object/bug/bug-0"
    api_call = get(api_call_url, timeout=5)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert database_object["title"] == "new bug", f"title value equals {database_object['title']}"
    assert database_object["description"] == "bug description", f"description value equals " \
                                                                f"{database_object['description']}"
    assert database_object["project_id"] == "proj-0", f"project_id value equals {database_object['project_id']}"
    assert database_object["parent"] == "tc-0", f"parent value equals {database_object['parent']}"


@mark.smoke
def test__smoke__api__get_objects__all_items(two_objects_of_type_database_fixture):
    api_call_url = "http://exultant_rhino_api:8101/get_objects/bug"
    api_call = get(api_call_url, timeout=5)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert len(database_object) == 2, f"Expected: 2, actual: {len(database_object)}"


@mark.smoke
def test__smoke__api__get_objects__filtered(two_objects_of_type_database_fixture):
    api_call_url = "http://exultant_rhino_api:8101/get_objects/bug?description=test"
    api_call = get(api_call_url, timeout=5)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert len(database_object) == 1, f"Expected: 1, actual: {len(database_object)}"
