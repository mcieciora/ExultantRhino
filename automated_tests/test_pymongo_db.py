from pytest import mark


@mark.unittests
def test__insert_and_find_one_record(test_db):
    """
    Verifies: REQ-DB1
    Verifies: REQ-DB2
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {'name': 'new_insert', 'value': 'test_value'}
    assert test_db.insert(test_data) != -1, 'Inserted object return id is -1'
    assert len(test_db.find(test_data)) == 1, 'Size of returned query is not equal 1'


@mark.unittests
def test__delete_and_find_no_records(test_db):
    """
    Verifies: REQ-DB1
    Verifies: REQ-DB2
    Verifies: REQ-DB3
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {'name': 'new_insert', 'value': 'test_value'}
    assert test_db.insert(test_data) != -1, 'Inserted object return id is -1'
    assert test_db.delete(test_data) == 1, 'Deletion was not acknowledged'
    assert len(test_db.find(test_data)) == 0, 'Size of returned query is not equal 1'


@mark.unittests
def test__delete_nonexistent_record(test_db):
    """
    Verifies: REQ-DB3
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {'name': 'new_insert', 'value': 'test_value'}
    assert test_db.delete(test_data) == 0, 'Deletion was not acknowledged'


@mark.unittests
def test__insert_and_update_one_record(test_db):
    """
    Verifies: REQ-DB1
    Verifies: REQ-DB2
    Verifies: REQ-DB4
    :param test_db: MongoDb object; taken from fixture
    :return: None
    """
    test_data = {'name': 'new_insert', 'value': 'test_value'}
    new_data = {'name': 'new_update', 'value': 'new_value'}
    assert test_db.insert(test_data) != -1, 'Inserted object return id is -1'
    assert len(test_db.find(test_data)) == 1, 'Size of returned query is not equal 1'
    assert test_db.update(test_data, {'$set': new_data}) == 1, 'Update was not acknowledged'
