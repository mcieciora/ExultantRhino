from pytest import fixture
from src.pymongo_db import MongoDb


@fixture(scope='function')
def test_db():
    test_db = MongoDb('test_db', 'test_collection')
    yield test_db
    test_db.client['test_db'].drop_collection('test_collection')
