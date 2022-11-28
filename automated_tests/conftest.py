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
    gecko_proc = Popen(["tools/geckodriver"], stdout=PIPE, shell=True)
    options = Options()
    options.headless = True
    test_driver = Firefox(options=options)
    test_driver.get('http://localhost:8000')
    yield test_driver
    test_driver.close()
    gecko_proc.kill()
