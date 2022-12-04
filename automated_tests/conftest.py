from subprocess import Popen, PIPE
from pytest import fixture
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from src.pymongo_db import MongoDb


@fixture(scope='function')
def test_db():
    """
    Test fixture yielding MongoDb object with 'test_db' database and 'test_collection' collection
    :return: MongoDb object
    """
    return_database = MongoDb('test_db', 'test_collection')
    yield return_database
    return_database.client['test_db'].drop_collection('test_collection')


@fixture(scope='function')
def firefox_driver():
    """
    Test fixture yielding Firefox webdriver for app frontend tests
    :return: Firefox webdriver from selenium library
    """
    with Popen(["tools/geckodriver"], stdout=PIPE, shell=True):
        options = Options()
        # options.headless = True
        test_driver = Firefox(options=options)
        test_driver.get('http://localhost:8000')
        yield test_driver
        test_driver.close()


@fixture(scope='session')
def test_upload_db():
    """
    Test fixture yielding MongoDb object with data needed for upload tests
    :return: MongoDb object
    """
    return_database = MongoDb('exultant_rhino', 'main_collection')
    insert_data = [
        {'object_type': 'requirement', 'title': 'req_1', 'description': 'desc', 'parent': 'OBJ-1: new_proj',
         'parent_project': 'new_proj', 'object_id': 'OBJ-50'},
        {'object_type': 'requirement', 'title': 'req_2', 'description': 'desc', 'parent': 'OBJ-1: new_proj',
         'parent_project': 'new_proj', 'object_id': 'OBJ-51'},
        {'object_type': 'requirement', 'title': 'req_3', 'description': 'desc', 'parent': 'OBJ-1: new_proj',
         'parent_project': 'new_proj', 'object_id': 'OBJ-52'},
        {'object_type': 'testcase', 'title': 'tc_1', 'description': 'desc', 'parent': 'OBJ-50: req_1',
         'parent_project': 'new_proj', 'object_id': 'OBJ-53'},
        {'object_type': 'testcase', 'title': 'tc_2', 'description': 'desc', 'parent': 'OBJ-50: req_1',
         'parent_project': 'new_proj', 'object_id': 'OBJ-54'},
        {'object_type': 'testcase', 'title': 'tc_3', 'description': 'desc', 'parent': 'OBJ-51: req_2',
         'parent_project': 'new_proj', 'object_id': 'OBJ-55'},
    ]
    for data in insert_data:
        return_database.insert(data)
    yield return_database
