from pytest import mark
from src.postgres_sql_alchemy import get_all_objects_by_type, get_objects_by_filters, get_database_object, \
    get_next_shortname
from src.postgres_items_models import Bug, Project, Release, Requirement, TestCase


@mark.smoke
def test__smoke__postgres__get_next_shortname__empty_database(empty_database_fixture):
    expected_values = ["proj-0", "rls-0", "req-0", "tc-0", "bug-0"]
    for index, database_object in enumerate([Project, Release, Requirement, TestCase, Bug]):
        actual_value = get_next_shortname(database_object)
        expected_value = expected_values[index]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.smoke
def test__smoke__postgres__get_next_shortname(one_object_of_type_database_fixture):
    expected_values = ["proj-1", "rls-1", "req-1", "tc-1", "bug-1"]
    for index, database_object in enumerate([Project, Release, Requirement, TestCase, Bug]):
        actual_value = get_next_shortname(database_object)
        expected_value = expected_values[index]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.smoke
def test__smoke__postgres__get_database_object__empty_database(empty_database_fixture):
    expected_value = {}
    actual_value = get_database_object(Project, "proj-0")
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value['title']}"


@mark.smoke
def test__smoke__postgres__get_database_object(one_object_of_type_database_fixture):
    test_data = {Project: "proj-0", Release: "rls-0", Requirement: "req-0", TestCase: "tc-0", Bug: "bug-0"}
    for object_type, shortname in test_data.items():
        expected_value = f"new {object_type.__name__.lower()}"
        actual_value = get_database_object(object_type, shortname)
        assert actual_value["title"] == expected_value, f"Expected: {expected_value}, actual: {actual_value['title']}"


@mark.smoke
def test__smoke__postgres__get_all_objects_by_type(two_objects_of_type_database_fixture):
    test_data = [Release, Requirement, TestCase, Bug]
    for object_type in test_data:
        expected_values = [f"{object_type.__name__.lower()} description", "test_description"]
        function_result = get_all_objects_by_type(object_type)
        assert len(function_result) == 2, f"Expected: 2, actual: {len(function_result)}"
        for index, database_object in enumerate(function_result):
            actual_result = database_object["description"]
            expected_result = expected_values[index]
            assert actual_result == expected_result, f"Expected: {expected_result}, actual: {actual_result}"


@mark.smoke
def test__smoke__postgres__get_objects_by_filters(two_objects_of_type_database_fixture):
    function_result = get_objects_by_filters(TestCase, {"description": "test_description"})
    expected_value = 1
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
    expected_value = "tc-1"
    actual_value = function_result[0]
    assert actual_value["shortname"] == expected_value, \
        f"Expected: {expected_value}, actual: {actual_value['shortname']}"
