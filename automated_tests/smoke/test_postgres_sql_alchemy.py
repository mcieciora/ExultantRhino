from pytest import mark
from src.postgres_sql_alchemy import get_next_shortname
from src.postgres_models import Bug, Project, Release, Requirement, TestCase


@mark.smoke
def test__smoke__postgres__get_next_shortname__empty_database(empty_database_fixture):
    expected_values = ["proj-0", "rls-0", "req-0", "tc-0", "bug-0"]
    for index, database_object in enumerate([Project, Release, Requirement, TestCase, Bug]):
        actual_value = get_next_shortname(database_object(title="test_object"))
        expected_value = expected_values[index]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.smoke
def test__smoke__postgres__get_next_shortname(one_object_database_fixture):
    expected_values = ["proj-1", "rls-1", "req-1", "tc-1", "bug-1"]
    for index, database_object in enumerate([Project, Release, Requirement, TestCase, Bug]):
        actual_value = get_next_shortname(database_object(title="test_object"))
        expected_value = expected_values[index]
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
