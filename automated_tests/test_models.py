from pytest import mark
from src.models import Models


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
    expected_data = {'project_id': 'PROJ-0', 'title': 'Template', 'object_type': 'project'}
    assert list(test_models.mongo.find({'object_type': 'project'}))[0] == expected_data, \
        'Template project has wrong attributes values'


@mark.unittests
def test__get_next_id_empty_database():
    """
    Verifies: REQ-MOD2
    :return: None
    """
    test_models = Models()
    assert test_models.get_next_id('bug', test_models.models['bug']) == 'BUG-0', \
        'Wrong id has been returned'


@mark.unittests
def test__get_next_id():
    """
    Verifies: REQ-MOD2
    :return: None
    """
    test_models = Models()
    assert test_models.get_next_id('project', test_models.models['project']) == 'PROJ-1', 'Wrong id has been returned'


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
    assert database_object['project_id'].startswith('PROJ-'), 'Object has got wrong id prefix'


@mark.unittests
def test__get_current_project_id():
    """
    Verifies: REQ-MOD4
    :return: None
    """
    test_models = Models()
    assert test_models.get_current_project_id()['project_id'] == 'PROJ-0', \
        'Wrong current project data has been returned'


@mark.unittests
def test__update_current_project_id():
    """
    Verifies: REQ-MOD4
    :return: None
    """
    test_models = Models()
    test_models.update_current_project_id('PROJ-1')
    assert test_models.project_pointer == 'PROJ-1', 'Project pointer has not been set'


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
    test_bug = {'title': 'new_bug', 'description': 'this is new bug', 'object_type': 'bug', 'parent': 'TC-0',
                'parent_project': 'PROJ-0'}
    test_models.create(test_bug)
    database_object = list(test_models.mongo.find({'object_type': 'bug'}))[0]
    for key, value in test_bug.items():
        assert value == database_object[key], 'Object database value is incorrect'
    assert database_object['bug_id'].startswith('BUG-'), 'Object has got wrong id prefix'


@mark.unittests
def test__get_next_id_new_bug_object():
    """
    Verifies: REQ-MOD2
    :return: None
    """
    test_models = Models()
    assert test_models.get_next_id('bug', test_models.models['bug']) == 'BUG-1', 'Wrong id has been returned'
