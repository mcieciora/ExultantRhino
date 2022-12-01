from pytest import mark
from requests import post
from json import dumps
from src.models import Models

# regular call
# non existing reqs in database
# non existing reqs in post request
# non existing tcs in database
# non existing tcs in post request


def send_request(data):
    url = "http://localhost:8000/upload"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return post(url, data=dumps(data), headers=headers)


@mark.upload
def test__empty_upload_data(test_upload_db):
    """
    Verifies: REQ-UP1
    Verifies: REQ-UP2
    :param test_upload_db: session fixture to create test data in database
    :return: None
    """
    test_models = Models()
    response = send_request({})
    assert response.status_code == 400, 'Wrong status code returned'
    assert not list(test_models.mongo.find({'object_type': 'release'})), 'Database should not contain release objects'
