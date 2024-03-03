from pytest import fixture
from src.postgres_sql_alchemy import Bug, create_database_object, drop_rows_by_table, Project, \
    Release, Requirement, TestCase, get_all_objects_by_type


def _insert_dummy_project():
    """
    Insert dummy project into database for testing purposes.
    :return: Committed object shortname value.
    """
    return create_database_object(Project(title="new project", description="description of new project"))


def _drop_all_rows():
    """
    Remove rows from all tables.
    """
    for object_type in [Project, Release, Requirement, TestCase, Bug]:
        drop_rows_by_table(object_type)


@fixture(scope="function")
def empty_database_fixture():
    """
    Fixture yields empty database.
    :return: Yielding empty database prepared for postgres and api testing.
    """
    _drop_all_rows()
    yield


@fixture(scope="function")
def one_object_database_fixture():
    """
    Fixture creates Release, Requirement, TestCase and Bug objects in database parenting them to proj-0 created by
    insert_dummy_project().
    :return: Yielding dummy database prepared for postgres and api testing.
    """
    project_shortname = _insert_dummy_project()
    parent_object = project_shortname
    object_types_list = [Release, Requirement, TestCase, Bug]
    for object_type in object_types_list:
        template_object_dict = {"title": f"new {object_type.__name__.lower()}", "project_id": project_shortname,
                                "description": f"{object_type.__name__.lower()} description", "parent": parent_object}
        new_db_object = object_type(**template_object_dict)
        parent_object = create_database_object(new_db_object)
    yield
    _drop_all_rows()
