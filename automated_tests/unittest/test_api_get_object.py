from pytest import mark
from src.api import get_object, get_objects


@mark.unittest
def test__unittest__api__get_object(mocker):
    mocker.patch(
        "src.api.get_database_object",
        return_value=[{"id": "None", "title": "project one", "shortname": "proj-1",
                       "description": "description of project one"}]
    )
    expected_value = '[{"id": "None", "title": "project one", "shortname": "proj-1", ' \
                     '"description": "description of project one"}]'
    actual_value = get_object("project", "proj-1")
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.unittest
def test__unittest__api__get_objects(mocker):
    mocker.patch("bottle.BaseRequest.params",
                 return_value={"shortname": "bug-1", "parent": "tc-2"})
    mocker.patch("src.api.get_objects_by_filters",
                 return_value=[{"id": "None", "title": "bug one", "shortname": "bug-1",
                                "description": "description of bug one", "parent": "tc-2"}])
    expected_value = '[{"id": "None", "title": "bug one", "shortname": "bug-1", ' \
                     '"description": "description of bug one", "parent": "tc-2"}]'
    actual_value = get_objects("bug")
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.unittest
def test__unittest__api__get_objects__empty_params(mocker):
    mocker.patch("bottle.BaseRequest.params",
                 return_value=False)
    mocker.patch("src.api.get_all_objects_by_type",
                 return_value=[{"id": "None", "title": "bug one", "shortname": "bug-1",
                                "description": "description of bug one", "parent": "tc-2"},
                               {"id": "None", "title": "bug two", "shortname": "bug-2",
                                "description": "description of bug two", "parent": "tc-2"}])
    expected_value = '[{"id": "None", "title": "bug one", "shortname": "bug-1", ' \
                     '"description": "description of bug one", "parent": "tc-2"}, ' \
                     '{"id": "None", "title": "bug two", "shortname": "bug-2", ' \
                     '"description": "description of bug two", "parent": "tc-2"}]'
    actual_value = get_objects("bug")
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
