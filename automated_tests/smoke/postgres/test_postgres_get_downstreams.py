from pytest import mark
from src.postgres_sql_alchemy import get_downstream_items
from src.postgres_items_models import Bug, Project, Release, Requirement, TestCase


@mark.smoke
def test__smoke__postgres__get_downstream_items__projects_return_with_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(Project, "proj-0", include_parent=True)]
    expected_values = ["proj-0", "rls-0", "rls-1", "req-0", "req-1", "req-2", "tc-0", "tc-1", "tc-2", "tc-3", "tc-4",
                       "bug-0", "bug-1"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."


@mark.smoke
def test__smoke__postgres__get_downstream_items__projects_return_without_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(Project, "proj-0")]
    expected_values = ["rls-0", "rls-1", "req-0", "req-1", "req-2", "tc-0", "tc-1", "tc-2", "tc-3", "tc-4", "bug-0",
                       "bug-1"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."


@mark.smoke
def test__smoke__postgres__get_downstream_items__release_return_with_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(Release, "rls-0", include_parent=True)]
    expected_values = ["rls-0", "req-0", "tc-0", "tc-1", "bug-0"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."

    function_result = [item["shortname"] for item in get_downstream_items(Release, "rls-1", include_parent=True)]
    expected_values = ["rls-1", "req-1", "req-2", "tc-2", "tc-3", "tc-4", "bug-1"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."


@mark.smoke
def test__smoke__postgres__get_downstream_items__release_return_without_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(Release, "rls-0")]
    expected_values = ["req-0", "tc-0", "tc-1", "bug-0"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."

    function_result = [item["shortname"] for item in get_downstream_items(Release, "rls-1")]
    expected_values = ["req-1", "req-2", "tc-2", "tc-3", "tc-4", "bug-1"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."


@mark.smoke
def test__smoke__postgres__get_downstream_items__requirement_return_with_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(Requirement, "req-0", include_parent=True)]
    expected_values = ["req-0", "tc-0", "tc-1", "bug-0"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."

    function_result = [item["shortname"] for item in get_downstream_items(Requirement, "req-2", include_parent=True)]
    expected_values = ["req-2", "tc-3", "tc-4", "bug-1"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."


@mark.smoke
def test__smoke__postgres__get_downstream_items__requirement_return_without_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(Requirement, "req-0")]
    expected_values = ["tc-0", "tc-1", "bug-0"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."

    function_result = [item["shortname"] for item in get_downstream_items(Requirement, "req-2")]
    expected_values = ["tc-3", "tc-4", "bug-1"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."


@mark.smoke
def test__smoke__postgres__get_downstream_items__test_case_return_with_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(TestCase, "tc-0", include_parent=True)]
    expected_values = ["tc-0"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."

    function_result = [item["shortname"] for item in get_downstream_items(TestCase, "tc-3", include_parent=True)]
    expected_values = ["tc-3", "bug-1"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."


@mark.smoke
def test__smoke__postgres__get_downstream_items__test_case_return_without_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(TestCase, "tc-0")]
    expected_values = []

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."

    function_result = [item["shortname"] for item in get_downstream_items(TestCase, "tc-3")]
    expected_values = ["bug-1"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."


@mark.smoke
def test__smoke__postgres__get_downstream_items__bug_return_with_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(Bug, "bug-0", include_parent=True)]
    expected_values = ["bug-0"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."

    function_result = [item["shortname"] for item in get_downstream_items(Bug, "bug-1", include_parent=True)]
    expected_values = ["bug-1"]

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."


@mark.smoke
def test__smoke__postgres__get_downstream_items__bug_return_without_parent(one_fully_set_up_project):
    function_result = [item["shortname"] for item in get_downstream_items(Bug, "bug-0")]
    expected_values = []

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."

    function_result = [item["shortname"] for item in get_downstream_items(Bug, "bug-1")]
    expected_values = []

    expected_value = len(expected_values)
    actual_value = len(function_result)
    assert actual_value == expected_value, f"Expected: {expected_value}, actual: {actual_value}"

    for item in expected_values:
        assert item in expected_values, f"Expected key: {item} does not exist."
