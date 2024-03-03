from requests import get
from pytest import mark


@mark.smoke
def test__smoke__api__get_object(one_object_database_fixture):
    api_call_url = "http://localhost:8101/get_object/project/proj-0"
    api_call = get(api_call_url)
    assert api_call.status_code == 200, "Status code is not 200."
