import pytest
from pytest import mark
from src.models import Models, ProjectExistsError


@mark.unittests
def test__get_next_id_empty_database():
    """
    Verifies: REQ-MOD2
    :return: None
    """
    test_models = Models()
    assert test_models.get_next_id() == 'OBJ-1', \
        'Wrong id has been returned'


@mark.unittests
def test__empty_database():
    """
    Verifies: REQ-MOD1
    :return: None
    """
    test_models = Models()
    assert len(list(test_models.mongo.find({'object_type': 'project'}))) == 1, 'Template project was not created'


@mark.unittests
def test__verify_default_project():
    """
    Verifies: REQ-MOD1
    :return: None
    """
    test_models = Models()
    expected_data = {'object_id': 'OBJ-0', 'title': 'Template', 'object_type': 'project'}
    assert list(test_models.mongo.find({'object_type': 'project'}))[0] == expected_data, \
        'Template project has wrong attributes values'


@mark.unittests
def test__get_next_id():
    """
    Verifies: REQ-MOD2
    :return: None
    """
    test_models = Models()
    assert test_models.get_next_id() == 'OBJ-1', 'Wrong id has been returned'


@mark.unittests
def test__create_new_project():
    """
    Verifies: REQ-MOD2
    Verifies: REQ-MOD3
    :return: None
    """
    test_models = Models()
    test_project = {'title': 'new_proj', 'description': 'this is new proj', 'object_type': 'project'}
    test_models.create(test_project)
    database_object = list(test_models.mongo.find({'object_type': 'project'}))[1]
    for key, value in test_project.items():
        assert value == database_object[key], 'Object database value is incorrect'
    assert database_object['object_id'].startswith('OBJ-'), 'Object has got wrong id prefix'


@mark.unittests
def test__double_project_creation():
    """
    Verifies: REQ-MOD3
    :return: None
    """
    test_models = Models()
    test_project = {'title': 'new_proj', 'description': 'this is new proj', 'object_type': 'project'}
    with pytest.raises(ProjectExistsError):
        test_models.create(test_project)


@mark.unittests
def test__get_current_project_id():
    """
    Verifies: REQ-MOD4
    :return: None
    """
    test_models = Models()
    assert test_models.get_current_project_id()['object_id'] == 'OBJ-0', \
        'Wrong current project data has been returned'


@mark.unittests
def test__update_current_project_id():
    """
    Verifies: REQ-MOD4
    :return: None
    """
    test_models = Models()
    test_models.update_current_project_id('OBJ-1')
    assert test_models.project_pointer == 'OBJ-1', 'Project pointer has not been set'


@mark.unittests
def test__get_all_projects():
    """
    Verifies: REQ-MOD5
    :return: None
    """
    test_models = Models()
    assert len(test_models.get_all_projects()) == 2, 'List of project has got wrong size'


@mark.unittests
def test__create_new_object():
    """
    Verifies: REQ-MOD2
    Verifies: REQ-MOD3
    :return: None
    """
    test_models = Models()
    test_bug = {'title': 'new_bug', 'description': 'this is new bug', 'object_type': 'bug', 'parent': 'OBJ-10',
                'parent_project': 'OBJ-0'}
    test_models.create(test_bug)
    database_object = list(test_models.mongo.find({'object_type': 'bug'}))[0]
    for key, value in test_bug.items():
        assert value == database_object[key], 'Object database value is incorrect'
    assert database_object['object_id'].startswith('OBJ-'), 'Object has got wrong id prefix'


@mark.unittests
def test__get_next_id_new_bug_object():
    """
    Verifies: REQ-MOD2
    :return: None
    """
    test_models = Models()
    assert test_models.get_next_id() == 'OBJ-3', 'Wrong id has been returned'


@mark.unittests
def test__edit_object():
    """
    Verifies: REQ-MOD4
    :return: None
    """
    test_bug = {'title': 'edited_bug', 'description': 'this is edited bug', 'object_type': 'testcase',
                'parent': 'OBJ-5', 'parent_project': 'OBJ-1'}
    test_models = Models()
    test_models.edit('OBJ-2', test_bug)
    database_object = list(test_models.mongo.find({'object_id': 'OBJ-2'}))[0]
    for key, value in database_object.items():
        if key in test_bug:
            assert test_bug[key] == value, 'Object has got incorrect values after edition.'
