from os import environ
from src.postgres_sql_alchemy import Bug, create_database_object, drop_rows_by_table, get_database_object, \
    get_objects_by_filters, Project, Release, Requirement, TestCase


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
    base_url = f"http://{environ['API_HOST']}:8501/+Create?item="

    return f"{base_url}{get_item_shortname_by_title(object_type, title)}"
