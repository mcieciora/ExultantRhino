from pytest import mark, raises
from src.models import Model, ModelCreationFailure, ModelValidationFailureKeys, ModelValidationFailureValues


@mark.unittests
def test__model_creation_failure_empty_model():
    """
    Verifies: REQ-MO1
    :return: None
    """
    with raises(ModelCreationFailure):
        Model({})


@mark.unittests
def test__model_creation_failure_wrong_values_types():
    """
    Verifies: REQ-MO1
    :return: None
    """
    with raises(ModelCreationFailure):
        Model({'name': 'str', 'user_id': int, 'closed': bool})


@mark.unittests
def test__validate_model():
    """
    Verifies: REQ-MO2
    :return: None
    """
    test_model = Model({'name': str, 'user_id': int, 'closed': bool})
    test_data = {'name': 'test_name', 'user_id': 0, 'closed': False}
    assert test_model.validate(test_data) == test_data, ''


@mark.unittests
def test__validation_failures_keys():
    """
    Verifies: REQ-MO2
    :return: None
    """
    test_model = Model({'name': str, 'user_id': int, 'closed': bool})
    test_data = {'wrong_name': 'test_name', 'user_id': 0, 'closed': False}
    with raises(ModelValidationFailureKeys):
        test_model.validate(test_data)


@mark.unittests
def test__validation_failures_values():
    """
    Verifies: REQ-MO2
    :return: None
    """
    test_model = Model({'name': str, 'user_id': int, 'closed': bool})
    test_data = {'name': 0, 'user_id': 'test_name', 'closed': False}
    with raises(ModelValidationFailureValues):
        test_model.validate(test_data)
