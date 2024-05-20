from requests import get
from pytest import mark


@mark.skip
@mark.smoke
def test__smoke__api__status():
    api_call_url = "http://exultant_rhino_api:8101/status"
    for expected_key in ["app_status", "api_status", "db_status"]:
        assert expected_key in get(api_call_url, timeout=5).text, f"{expected_key} not available in request response"
