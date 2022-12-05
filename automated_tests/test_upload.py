from json import dumps
from pytest import mark
from requests import post, get


def send_request(data):
    url = "http://localhost:8000/upload"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    return post(url, data=dumps(data), headers=headers, timeout=5)


@mark.upload
def test__empty_upload_data(test_upload_db):
    """
    Verifies: REQ-UP1
    Verifies: REQ-UP2
    :param test_upload_db: session fixture to create test data in database
    :return: None
    """
    response = send_request({})
    assert response.status_code == 400, 'Wrong status code returned'
    assert not test_upload_db.find({'object_type': 'release'}), 'Database should not contain release objects'


@mark.upload
def test__regular_upload_data(test_upload_db):
    """
    Verifies: REQ-UP1
    Verifies: REQ-UP2
    Verifies: REQ-UP3
    :param test_upload_db: session fixture to create test data in database
    :return: None
    """
    get('http://localhost:8000/proj/OBJ-1', timeout=5)
    response = send_request({
        'project_name': 'new_proj', 'release_name': 'test_name_1', 'reqs': {
            'OBJ-50': {'OBJ-53': 'pass', 'OBJ-54': 'fail'}
        }
    })
    expected_values = {'OBJ-51': {'OBJ-55': 'not_run'}, 'OBJ-52': {}}
    assert response.status_code == 200, 'Wrong status code returned'
    database_objects = test_upload_db.find({'title': 'test_name_1'})[0]['requirements']
    assert database_objects['OBJ-50'] == \
           {'OBJ-53': 'pass', 'OBJ-54': 'fail'}, 'Release has not been added properly.'
    for key, value in expected_values.items():
        assert database_objects[key] == value, 'Other values were touched but should not'


@mark.upload
def test__non_existing_req_in_post_request(test_upload_db):
    """
    Verifies: REQ-UP1
    Verifies: REQ-UP2
    :param test_upload_db: session fixture to create test data in database
    :return: None
    """
    get('http://localhost:8000/proj/OBJ-1', timeout=5)
    response = send_request({
        'project_name': 'new_proj', 'release_name': 'test_name_2', 'reqs': {
            'OBJ-X': {'OBJ-53': 'pass', 'OBJ-54': 'fail'}
        }
    })
    expected_values = {'OBJ-50': {'OBJ-53': 'not_run', 'OBJ-54': 'not_run'},
                       'OBJ-51': {'OBJ-55': 'not_run'}, 'OBJ-52': {}}
    assert response.status_code == 200, 'Wrong status code returned'
    database_objects = test_upload_db.find({'title': 'test_name_2'})[0]['requirements']
    for key, value in expected_values.items():
        assert database_objects[key] == value, 'Other values were touched but should not'


@mark.upload
def test__check_number_of_results(test_upload_db):
    """
    Verifies: REQ-UP2
    Verifies: REQ-UP3
    :param test_upload_db: session fixture to create test data in database
    :return: None
    """
    get('http://localhost:8000/proj/OBJ-1', timeout=5)
    response = send_request({
        'project_name': 'new_proj', 'release_name': 'test_name_3', 'reqs': {
            'OBJ-50': {'OBJ-53': 'pass', 'OBJ-54': 'fail'},
            'OBJ-51': {'OBJ-55': 'not_run'},
        }
    })
    expected_values = {'fail': 1, 'pass': 1, 'not_run': 1}
    assert response.status_code == 200, 'Wrong status code returned'
    database_objects = test_upload_db.find({'title': 'test_name_3'})[0]['results']
    assert database_objects == expected_values
