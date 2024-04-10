from pytest import mark
from src.postgres_sql_alchemy import create_database_object, delete_database_object, drop_rows_by_table, \
    edit_database_object, get_all_objects_by_type, get_database_object
from src.postgres_models import Bug


@mark.smoke
def test__smoke__postgres__create_database_object(one_object_of_type_database_fixture):
    test_data = Bug(title="new bug", description="description of new bug", project_id="proj-0", parent="proj-0")
    actual_value = create_database_object(test_data)
    expected_value = "bug-1"
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
    actual_value = get_all_objects_by_type(Bug)
    expected_value = 2
    assert len(actual_value) == expected_value, f"Expected: {expected_value}, actual: {len(actual_value)}"


@mark.smoke
def test__smoke__postgres__edit_database_object(one_object_of_type_database_fixture):
    test_object = get_database_object(Bug, "bug-0")
    new_data = {"title": "edited title", "parent": "tc-1"}
    edit_database_object(Bug, test_object["id"], new_data)
    actual_value = get_database_object(Bug, "bug-0")
    assert actual_value["title"] == new_data["title"], f"Expected: {new_data['title']}, actual: {actual_value['title']}"
    assert actual_value["parent"] == new_data["parent"], \
        f"Expected: {new_data['parent']}, actual: {actual_value['parent']}"


@mark.smoke
def test__smoke__postgres__delete_database_object(one_object_of_type_database_fixture):
    test_object = get_database_object(Bug, "bug-0")
    delete_database_object(Bug, test_object["id"])
    actual_value = get_all_objects_by_type(Bug)
    assert len(actual_value) == 0, f"Expected: 0, actual: {len(actual_value)}"


@mark.smoke
def test__smoke__postgres__drop_rows_by_table(two_objects_of_type_database_fixture):
    drop_rows_by_table(Bug)
    actual_value = get_all_objects_by_type(Bug)
    assert len(actual_value) == 0, f"Expected: 0, actual: {len(actual_value)}"
