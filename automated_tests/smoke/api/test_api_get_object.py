from requests import get
from pytest import mark


@mark.smoke
def test__smoke__api__get_object_by_shortname__project(one_object_of_type_database_fixture):
    api_call_url = "http://exultant_rhino_api:8101/get/project/proj-0"
    api_call = get(api_call_url, timeout=5)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert database_object["title"] == "new project", f"title value equals {database_object['title']}"
    assert database_object["description"] == "description of new project", f"description value equals " \
                                                                           f"{database_object['description']}"


@mark.smoke
def test__smoke__api__get_object_by_shortname__bug(one_object_of_type_database_fixture):
    api_call_url = "http://exultant_rhino_api:8101/get/bug/bug-0"
    api_call = get(api_call_url, timeout=5)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert database_object["title"] == "new bug", f"title value equals {database_object['title']}"
    assert database_object["description"] == "bug description", f"description value equals " \
                                                                f"{database_object['description']}"
    assert database_object["project_shortname"] == "proj-0", f"project_shortname value equals " \
                                                             f"{database_object['project_shortname']}"
    assert database_object["parent"] == "tc-0", f"parent value equals {database_object['parent']}"


@mark.smoke
def test__smoke__api__get__all_items(two_objects_of_type_database_fixture):
    api_call_url = "http://exultant_rhino_api:8101/get/bug"
    api_call = get(api_call_url, timeout=5)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert len(database_object) == 2, f"Expected: 2, actual: {len(database_object)}"


@mark.smoke
def test__smoke__api__get__filtered(two_objects_of_type_database_fixture):
    api_call_url = "http://exultant_rhino_api:8101/get/bug?description=test"
    api_call = get(api_call_url, timeout=5)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert len(database_object) == 1, f"Expected: 1, actual: {len(database_object)}"
