from requests import get
from pytest import mark


@mark.smoke
def test__smoke__insert_object(empty_database_fixture):
    api_call_url = "http://localhost:8101/insert_object/project?title=new+proj"
    api_call = get(api_call_url)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert database_object["committed_shortname"] == "proj-0", f"committed_shortname equals " \
                                                               f"{database_object['committed_shortname']}"
