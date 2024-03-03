from pytest import mark
from src.postgres_sql_alchemy import convert_to_dict, get_all_objects_by_type, get_next_shortname
from src.postgres_models import Bug, Project, Release, Requirement, TestCase


@mark.unittest
def test__unittest__postgres__convert_to_dict():
    expected_value = {"id": None,
                      "shortname": None,
                      "title": f"new project",
                      "description": f"Project description"}
    database_object = Project(title="new project", description="Project description")
    actual_value = convert_to_dict(database_object)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
    expected_value = {"id": None,
                      "shortname": None,
                      "title": f"new release",
                      "description": f"Release description",
                      "project_id": "proj-0",
                      "parent": "proj-0"}
    database_object = Release(title="new release", description="Release description", project_id="proj-0",
                              parent="proj-0")
    actual_value = convert_to_dict(database_object)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.unittest
def test__unittest__postgres__get_next_shortname_empty(mocker):
    mocker.patch(
        "src.postgres_sql_alchemy.get_all_objects_by_type",
        return_value=[]
    )
    for object_type in [Bug, Project, Release, Requirement, TestCase]:
        expected_value = {Project: "proj-0", Release: "rls-0", Requirement: "req-0", TestCase: "tc-0",
                          Bug: "bug-0"}[object_type]
        actual_value = get_next_shortname(object_type)
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.unittest
def test__unittest__postgres__get_next_shortname(mocker):
    mocker.patch(
        "src.postgres_sql_alchemy.get_all_objects_by_type",
        return_value=[{"id": 0, "shortname": "proj-0", "title": "new project", "description": "description"},
                      {"id": 0, "shortname": "rls-0", "title": "new release", "description": "description"},
                      {"id": 0, "shortname": "req-0", "title": "new requirement", "description": "description"},
                      {"id": 0, "shortname": "tc-0", "title": "new testcase", "description": "description"},
                      {"id": 0, "shortname": "bug-0", "title": "new bug", "description": "description"}]
    )
    for object_type in [Bug, Project, Release, Requirement, TestCase]:
        expected_value = {Project: "proj-1", Release: "rls-1", Requirement: "req-1", TestCase: "tc-1",
                          Bug: "bug-1"}[object_type]
        actual_value = get_next_shortname(object_type)
        assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"


@mark.unittest
def test__unittest__postgres__get_all_objects_by_type(mocker):
    postgres_session_mock = mocker.patch("src.postgres_sql_alchemy.get_session").return_value = mocker.Mock()
    postgres_session_mock.query.return_value.all.return_value = [
        Project(title="project one", shortname="proj-1", description="description of project one"),
        Project(title="project two", shortname="proj-2", description="description of project two")]
    actual_value = get_all_objects_by_type(Project)
    expected_value = [
        {"id": None, "title": "project one", "shortname": "proj-1", "description": "description of project one"},
        {"id": None, "title": "project two", "shortname": "proj-2", "description": "description of project two"}]
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"
