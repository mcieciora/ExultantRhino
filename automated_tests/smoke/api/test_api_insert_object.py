from requests import get
from pytest import mark


@mark.skip
@mark.smoke
def test__smoke__insert(empty_database_fixture_function):
    api_call_url = "http://exultant_rhino_api:8101/insert/project?title=new+proj"
    api_call = get(api_call_url, timeout=5)
    assert api_call.status_code == 200, "Status code is not 200."
    database_object = api_call.json()
    assert database_object["committed_shortname"] == "proj-0", f"committed_shortname equals " \
                                                               f"{database_object['committed_shortname']}"
