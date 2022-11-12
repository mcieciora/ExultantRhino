from pytest import fixture
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
