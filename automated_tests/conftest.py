from pytest import fixture
from src.postgres_sql_alchemy import Bug, create_database_object, Project, Release, Result, Requirement, TestCase
from automated_tests.postgres_util import _drop_all_rows, _insert_dummy_project
from automated_tests.selenium_util import SeleniumUtil


@fixture(scope="function")
def selenium_util():
    """
    Fixture opens browser window with exultant rhino app.

    :return: Yielding browser app.
    """
    selenium_util = SeleniumUtil()
    yield selenium_util
    selenium_util.terminate()


@fixture(scope="function")
def empty_database_fixture_function():
    """
    Empty database function fixture.

    :return: None
    """
    _drop_all_rows()
    yield
    _drop_all_rows()


@fixture(scope="module")
def empty_database_fixture_session():
    """
    Empty database session fixture.

    :return: None
    """
    _drop_all_rows()
    yield
    _drop_all_rows()


@fixture(scope="function")
def one_object_of_type_database_fixture():
    """
    Fixture creates rls, req, tc and bug objects in database parenting them to proj-0 created by insert_dummy_project().

    :return: Yielding dummy database prepared for postgres and api testing.
    """
    _drop_all_rows()
    project_shortname = _insert_dummy_project()
    parent_object = project_shortname
    object_types_list = [Release, Requirement, TestCase, Bug]
    for object_type in object_types_list:
        template_object_dict = {"title": f"new {object_type.__name__.lower()}", "project_shortname": project_shortname,
                                "description": f"{object_type.__name__.lower()} description", "parent": parent_object}
        new_db_object = object_type(**template_object_dict)
        parent_object = create_database_object(new_db_object)
    yield
    _drop_all_rows()


@fixture(scope="function")
def two_objects_of_type_database_fixture():
    """
    Fixture creates rls, req, tc and bug objects in database parenting them to proj-0 created by insert_dummy_project().

    :return: Yielding dummy database prepared for postgres and api testing.
    """
    _drop_all_rows()
    project_shortname = _insert_dummy_project()
    parent_object = project_shortname
    object_types_list = [Release, Requirement, TestCase, Bug]
    for object_type in object_types_list:
        for description in [f"{object_type.__name__.lower()} description", "test_description"]:
            template_object_dict = {"title": f"new {object_type.__name__.lower()}",
                                    "project_shortname": project_shortname,
                                    "description": f"{description}",
                                    "parent": parent_object}
            new_db_object = object_type(**template_object_dict)
            parent_object = create_database_object(new_db_object)
    yield
    _drop_all_rows()


@fixture(scope="module")
def two_projects_fixture():
    """
    Fixture creates two empty projects objects in database.

    :return: Yielding dummy database prepared for postgres and api testing.
    """
    _drop_all_rows()
    create_database_object(Project(title="first project", description="description of first project"))
    create_database_object(Project(title="second project", description="description of second project"))
    yield
    _drop_all_rows()


@fixture(scope="module")
def one_fully_set_up_project():
    """
    Fixture creates one full project tree.

    :return: Yielding None
    """
    _drop_all_rows()

    project_shortname = _insert_dummy_project()
    parent_object = project_shortname

    items_to_create = [
        Release(**{"title": "0_1", "project_shortname": parent_object, "description": "First release",
                   "parent": "proj-0"}),
        Release(**{"title": "0_2", "project_shortname": parent_object, "description": "Second release",
                   "parent": "proj-0"}),

        Requirement(**{"title": "req_1", "project_shortname": parent_object, "description": "req_1 description",
                       "parent": "rls-0", "target_release": "rls-0"}),
        Requirement(**{"title": "req_2", "project_shortname": parent_object, "description": "req_2 description",
                       "parent": "rls-1", "target_release": "rls-1"}),
        Requirement(**{"title": "req_3", "project_shortname": parent_object, "description": "req_3 description",
                       "parent": "rls-1", "target_release": "rls-1"}),

        TestCase(**{"title": "tc_1", "project_shortname": parent_object, "description": "tc_1 description",
                    "parent": "req-0", "target_release": "rls-0"}),
        TestCase(**{"title": "tc_2", "project_shortname": parent_object, "description": "tc_2 description",
                    "parent": "req-0", "target_release": "rls-0"}),
        TestCase(**{"title": "tc_3", "project_shortname": parent_object, "description": "tc_3 description",
                    "parent": "req-1", "target_release": "rls-1"}),
        TestCase(**{"title": "tc_4", "project_shortname": parent_object, "description": "tc_4 description",
                    "parent": "req-2", "target_release": "rls-1"}),
        TestCase(**{"title": "tc_5", "project_shortname": parent_object, "description": "tc_5 description",
                    "parent": "req-2", "target_release": "rls-1"}),

        Bug(**{"title": "bug_tc_2", "project_shortname": parent_object, "description": "bug_tc_2 description",
               "parent": "tc-1", "target_release": "rls-0"}),
        Bug(**{"title": "bug_tc_4", "project_shortname": parent_object, "description": "bug_tc_4 description",
               "parent": "tc-3", "target_release": "rls-1"}),
    ]

    for item in items_to_create:
        create_database_object(item)
    yield
    _drop_all_rows()


@fixture(scope="module")
def two_fully_set_up_projects():
    """
    Fixture creates two full projects tree.

    :return: Yielding None
    """
    _drop_all_rows()

    create_database_object(Project(title="DEFAULT", description="DEFAULT project"))
    create_database_object(Project(title="new_project", description="new_project description"))

    items_to_create = [
        Release(**{"title": "0_1", "project_shortname": "DEFAULT", "description": "First release",
                   "parent": "DEFAULT"}),
        Release(**{"title": "0_2", "project_shortname": "DEFAULT", "description": "Second release",
                   "parent": "DEFAULT"}),
        Release(**{"title": "alpha", "project_shortname": "new_project", "description": "alpha release",
                   "parent": "new_project"}),

        Requirement(**{"title": "req_1", "project_shortname": "DEFAULT", "description": "req_1 description",
                       "parent": "rls-0", "target_release": "rls-0"}),
        Requirement(**{"title": "req_2", "project_shortname": "DEFAULT", "description": "req_2 description",
                       "parent": "rls-0", "target_release": "rls-0"}),
        Requirement(**{"title": "req_3", "project_shortname": "DEFAULT", "description": "req_3 description",
                       "parent": "rls-1", "target_release": "rls-1"}),
        Requirement(**{"title": "alpha_1", "project_shortname": "new_project", "description": "alpha_1 description",
                       "parent": "rls-2", "target_release": "rls-2"}),
        Requirement(**{"title": "alpha_2", "project_shortname": "new_project", "description": "alpha_2 description",
                       "parent": "rls-2", "target_release": "rls-2"}),

        TestCase(**{"title": "tc_1", "project_shortname": "DEFAULT", "description": "tc_1 description",
                    "parent": "req-0", "target_release": "rls-0"}),
        TestCase(**{"title": "tc_2", "project_shortname": "DEFAULT", "description": "tc_2 description",
                    "parent": "req-0", "target_release": "rls-0"}),
        TestCase(**{"title": "tc_3", "project_shortname": "DEFAULT", "description": "tc_3 description",
                    "parent": "req-1", "target_release": "rls-0"}),
        TestCase(**{"title": "tc_4", "project_shortname": "DEFAULT", "description": "tc_4 description",
                    "parent": "req-2", "target_release": "rls-1"}),
        TestCase(**{"title": "tc_5", "project_shortname": "DEFAULT", "description": "tc_5 description",
                    "parent": "req-2", "target_release": "rls-1"}),
        TestCase(**{"title": "t1", "project_shortname": "new_project", "description": "t1 description",
                    "parent": "req-3", "target_release": "rls-2"}),
        TestCase(**{"title": "t2", "project_shortname": "new_project", "description": "t2 release",
                    "parent": "req-3", "target_release": "rls-2"}),
        TestCase(**{"title": "t3", "project_shortname": "new_project", "description": "t3 release",
                    "parent": "req-4", "target_release": "rls-2"}),

        Bug(**{"title": "bug_tc_2", "project_shortname": "DEFAULT", "description": "bug_tc_2 description",
               "parent": "tc-1", "target_release": "rls-0"}),
        Bug(**{"title": "bug_tc_4", "project_shortname": "DEFAULT", "description": "bug_tc_4 description",
               "parent": "tc-3", "target_release": "rls-1"}),
        Bug(**{"title": "bt1", "project_shortname": "new_project", "description": "bt1 description",
               "parent": "tc-5", "target_release": "rls-2"}),
        Bug(**{"title": "bt2", "project_shortname": "new_project", "description": "bt2 description",
               "parent": "tc-6", "target_release": "rls-2"})
    ]

    for item in items_to_create:
        create_database_object(item)
    yield
    _drop_all_rows()


@fixture(scope="function")
def multiple_not_covered_items():
    """
    Fixture creates tree consisting multiple not covered items of all types.

    :return: Yielding None
    """
    _drop_all_rows()

    create_database_object(Project(title="DEFAULT", description="DEFAULT project"))
    create_database_object(Project(title="new_project", description="DEFAULT project"))

    items_to_create = [
        Release(**{"title": "0_1", "project_shortname": "new_project", "description": "First release"}),
        Release(**{"title": "0_2", "project_shortname": "new_project", "description": "Second release"}),
        Release(**{"title": "0_3", "project_shortname": "new_project", "description": "Third release"}),
        Release(**{"title": "0_4", "project_shortname": "new_project", "description": "Fourth release"}),

        Requirement(**{"title": "req_1", "project_shortname": "new_project", "description": "req_1 description",
                       "parent": "rls-0", "target_release": "rls-0"}),
        Requirement(**{"title": "req_2", "project_shortname": "new_project", "description": "req_2 description",
                       "parent": "rls-0", "target_release": "rls-0"}),
        Requirement(**{"title": "req_3", "project_shortname": "new_project", "description": "req_3 description",
                       "parent": "rls-0", "target_release": "rls-0"}),
        Requirement(**{"title": "req_4", "project_shortname": "new_project", "description": "req_4 description",
                       "parent": "rls-0", "target_release": "rls-0"}),

        TestCase(**{"title": "tc_1", "project_shortname": "new_project", "description": "tc_1 description",
                    "parent": "req-0", "target_release": "rls-0"}),
        TestCase(**{"title": "tc_2", "project_shortname": "new_project", "description": "tc_2 description",
                    "parent": "req-0", "target_release": "rls-0"}),
        TestCase(**{"title": "tc_3", "project_shortname": "new_project", "description": "tc_3 description",
                    "parent": "req-0", "target_release": "rls-0"}),
        TestCase(**{"title": "tc_4", "project_shortname": "new_project", "description": "tc_4 description",
                    "parent": "req-0", "target_release": "rls-0"}),
        TestCase(**{"title": "tc_5", "project_shortname": "new_project", "description": "tc_5 description",
                    "parent": "req-0", "target_release": "rls-0"}),

        Bug(**{"title": "bug_1", "project_shortname": "new_project", "description": "bug_1 description",
               "parent": "tc-0", "target_release": "rls-0"}),
        Bug(**{"title": "bug_2", "project_shortname": "new_project", "description": "bug_2 description",
               "parent": "tc-0", "target_release": "rls-0"}),
        Bug(**{"title": "bug_3", "project_shortname": "new_project", "description": "bug_3 description",
               "parent": "tc-0", "target_release": "rls-0"}),
        Bug(**{"title": "bug_4", "project_shortname": "new_project", "description": "bug_4 description",
               "parent": "tc-0", "target_release": "rls-0"}),
    ]

    for item in items_to_create:
        create_database_object(item)
    yield
    _drop_all_rows()


@fixture(scope="session")
def multiple_results():
    """
    Fixture creates tree consisting multiple not covered items of all types.

    :return: Yielding None
    """
    _drop_all_rows()

    _insert_dummy_project()
    create_database_object(Result(title="develop_1", project_shortname="new project", build_url="", passed=100,
                                  failed=10, skipped=5))
    create_database_object(Result(title="develop_2", project_shortname="new project", build_url="", passed=100,
                                  failed=0, skipped=0))
    create_database_object(Result(title="develop_3", project_shortname="new project", build_url="", passed=0,
                                  failed=0, skipped=0))
    create_database_object(Result(title="develop_4", project_shortname="new project", build_url="", passed=0,
                                  failed=10, skipped=5))
    create_database_object(Result(title="develop_5", project_shortname="new project", build_url="", passed=1,
                                  failed=1, skipped=1))
    yield
    _drop_all_rows()
