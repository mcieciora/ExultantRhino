from pytest import mark
from src.models import Models


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
    assert len(test_models.mongo.find({'object_type': 'project'})) == 1, 'Template project was not created'


@mark.unittests
def test__verify_default_project():
    """
    Verifies: REQ-MOD1
    :return: None
    """
    test_models = Models()
    expected_data = {'object_id': 'OBJ-0', 'title': 'Template', 'object_type': 'project'}
    assert test_models.mongo.find({'object_type': 'project'})[0] == expected_data, \
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
    Verifies: REQ-MOD3
    :return: None
    """
    test_models = Models()
    expected_data = {'title': 'new_proj', 'description': 'this is new proj', 'object_type': 'project'}
    test_models.create({'title': 'new_proj', 'description': 'this is new proj', 'object_type': 'project'})
    database_object = test_models.mongo.find({'object_type': 'project'})[1]
    for key, value in expected_data.items():
        assert value == database_object[key], 'Object database value is incorrect'


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
    expected_data = {'title': 'new_bug', 'description': 'this is new bug', 'object_type': 'bug', 'parent': 'OBJ-10',
                     'parent_project': 'OBJ-0'}
    test_models.create({'title': 'new_bug', 'description': 'this is new bug', 'object_type': 'bug', 'parent': 'OBJ-10',
                        'parent_project': 'OBJ-0'})
    database_object = test_models.mongo.find({'object_type': 'bug'})[0]
    for key, value in expected_data.items():
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
    database_object = test_models.mongo.find({'object_id': 'OBJ-2'})[0]
    for key, value in database_object.items():
        if key in test_bug:
            assert test_bug[key] == value, 'Object has got incorrect values after edition.'


@mark.unittests
def test__delete_object():
    """
    Verifies: REQ-MOD5
    :return: None
    """
    test_models = Models()
    test_models.delete('OBJ-2')
    assert not test_models.mongo.find({'object_id': 'OBJ-2'}), 'Object was not deleted.'


@mark.unittests
def test__get_dependencies():
    """
    Verifies: REQ-MOD6
    :return: None
    """
    test_models = Models()
    test_data = {'requirement': {'amount': 1, 'pointer': 'OBJ-0: Template'},
                 'testcase': {'amount': 2, 'pointer': 'OBJ-2: new_requirement'},
                 'bug': {'amount': 1, 'pointer': 'OBJ-3: new_testcase'}}
    expected_data = {'requirement': {'amount': 2, 'pointer': 'OBJ-2: new_requirement'},
                     'testcase': {'amount': 1, 'pointer': 'OBJ-3: new_testcase'}}
    for key, value in test_data.items():
        for _ in range(0, value['amount']):
            test_models.create({'title': f'new_{key}', 'description': f'this is {key}', 'object_type': key,
                                'parent': value['pointer'], 'parent_project': 'Template'})
    for element, value in expected_data.items():
        test_dict = value
        assert len(test_models.get_dependencies(element)[test_dict['pointer'].split(':', maxsplit=1)[0]]) == \
               test_dict['amount'], 'Number of dependencies is incorrect'


@mark.unittests
def test__get_dependencies_extended_key():
    """
    Verifies: REQ-MOD6
    :return: None
    """
    test_models = Models()
    expected_data = {
        True: ['OBJ-3: new_testcase', 'OBJ-4: new_testcase'],
        False: ['OBJ-3', 'OBJ-4']
    }
    for bool_value, test_data in expected_data.items():
        assert test_data == list(test_models.get_dependencies('testcase', extended_key=bool_value).keys()), \
            'get_dependencies returned wrong keys'


@mark.unittests
def test__get_all_objects_of_type():
    """
    Verifies: REQ-MOD6
    :return: None
    """
    test_models = Models()
    test_data = {'bug': 1, 'project': 0, 'requirement': 1, 'testcase': 2}
    for key, value in test_data.items():
        assert len(test_models.get_all_objects_of_type(key)) == value, 'Number of objects is incorrect'


@mark.unittests
def test__get_test_case_requirements_dependencies():
    """
    Verifies: REQ-MOD6
    :return: None
    """
    test_models = Models()
    expected_data = {'OBJ-2': {'OBJ-3': 'not_run', 'OBJ-4': 'not_run'}}
    assert test_models.get_test_case_requirements_dependencies() == expected_data, \
        'Requirements dependency dicts are not the same'
