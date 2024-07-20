from os import environ
from src.postgres_sql_alchemy import Bug, create_database_object, drop_rows_by_table, get_objects_by_filters, \
    Project, Release, Result, Requirement, TestCase
from src.postgres_tasks_models import Task


def _insert_dummy_project():
    """
    Insert dummy project into database for testing purposes.

    :return: Committed object shortname value.
    """
    project_title = "new project"
    create_database_object(Project(title=project_title, description="description of new project"))
    return project_title


def _drop_all_rows():
    """Remove rows from all tables."""
    for object_type in [Project, Release, Result, Requirement, Task, TestCase, Bug]:
        drop_rows_by_table(object_type)


def get_item_shortname_by_title(object_type, title):
    """
    Get item shortname by provided title.

    :return: Item shortname.
    """
    item = get_objects_by_filters(object_type, {"title": title})[0]
    return item["shortname"]


def get_item_page_url_by_title(object_type, title):
    """
    Get item view page url by title.

    :return: Page view page url.
    """
    base_url = f"http://{environ['APP_HOST']}:8501/+Create?item="

    return f"{base_url}{get_item_shortname_by_title(object_type, title)}"
