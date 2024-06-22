from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import src.postgres_items_models as items_models
import src.postgres_tasks_models as tasks_models
from src.postgres_items_models import Bug, Project, Release, Requirement, TestCase
from src.postgres_tasks_models import Task


def _get_engine():
    """
    Get engine object with connection arguments taken from environment.
    :return: Engine class object.
    """
    return create_engine(
        f"postgresql://{environ['POSTGRES_USER']}:{environ['POSTGRES_PASSWORD']}@"
        f"{environ['DB_HOST']}:{environ['DB_PORT']}/{environ['POSTGRES_DB']}", pool_size=10
    )


Session = sessionmaker(bind=_get_engine())


def convert_to_dict(database_object):
    """
    Create dict out of given database object.
    :return: Database object dict.
    """
    try:
        return {
            column.name: getattr(database_object, column.name)
            for column in database_object.__table__.columns
        }
    except AttributeError:
        return {}


def get_next_shortname(object_type):
    """
    Get next object shortname value based on given object type.
    :return: String value in (proj/rls/req/tc/bug)-xxx format.
    """
    shortname_prefix = {
        Project: "proj",
        Release: "rls",
        Requirement: "req",
        TestCase: "tc",
        Bug: "bug",
        Task: "task"
    }
    try:
        last_object_id = max(
            map(lambda db_object: int(db_object["shortname"].split("-")[1]), get_all_objects_by_type(object_type)))
        return f"{shortname_prefix[object_type]}-{last_object_id + 1}"
    except ValueError:
        return f"{shortname_prefix[object_type]}-0"


def get_database_object(object_type, shortname):
    """
    Get database object by its type (Project, Release, Requirement, TestCase, Bug) and shortname
    in (proj/rls/req/tc/bug)-xxx format.
    :return: Database object.
    """
    with Session.begin() as session:
        database_object = (
            session.query(object_type).filter_by(shortname=shortname).first()
        )
        return convert_to_dict(database_object)


def get_all_objects():
    """
    Get list of all database objects.
    :return: List of database objects.
    """
    all_objects = []
    for object_type in [Project, Release, Requirement, TestCase, Bug]:
        all_objects.extend(get_all_objects_by_type(object_type))
    return all_objects


def get_all_objects_by_type(object_type):
    """
    Get list of database objects by their type (Project, Release, Requirement, TestCase, Bug).
    :return: List of database objects.
    """
    with Session.begin() as session:
        return [
            convert_to_dict(db_object)
            for db_object in session.query(object_type).all()
        ]


def get_all_objects_with_filters(object_types, filters_dict):
    """
    Get list of all database objects.
    :return: List of database objects.
    """
    all_objects = []
    for object_type in object_types:
        all_objects.extend(get_objects_by_filters(object_type, filters_dict))
    return all_objects


def get_objects_by_filters(object_type, filters_dict):
    """
    Get list of database objects by their type (Project, Release, Requirement, TestCase, Bug)
    and filtered by given query.
    :return: List of database objects.
    """
    with Session.begin() as session:
        query = session.query(object_type)
    for key, value in filters_dict.items():
        query = query.filter(getattr(object_type, key).like("%%%s%%" % value)).all()
    return [convert_to_dict(db_object) for db_object in query]


def get_downstream_items(parent_item_type, shortname, include_parent=False):
    """
    Get list of downstream items of given object.
    :return: List of downstream items.
    """
    all_items_types = [Project, Release, Requirement, TestCase, Bug]
    parent_item = get_database_object(parent_item_type, shortname)
    downstream_list = [parent_item]
    downstream_items = [parent_item]

    starting_index = all_items_types.index(parent_item_type)+1

    for target_type in all_items_types[starting_index::]:
        _temp_list = []
        for item in downstream_items:
            _temp_list.extend(get_objects_by_filters(target_type, {"parent": item["shortname"]}))
        downstream_items = _temp_list
        downstream_list.extend(downstream_items)
    if not include_parent:
        downstream_list.remove(parent_item)
    return downstream_list


def create_database_object(object_to_commit):
    """
    Create database object from given dictionary.
    :return: Committed object shortname value.
    """
    with Session.begin() as session:
        setattr(object_to_commit, "shortname", get_next_shortname(type(object_to_commit)))
        session.add(object_to_commit)
        return object_to_commit.shortname


def edit_database_object(object_type, object_id, new_data):
    """
    Edit database object by providing dict of new values.
    :return: None
    """
    with Session.begin() as session:
        db_object = session.get(object_type, object_id)
        for key, value in new_data.items():
            setattr(db_object, key, value)


def delete_database_object(object_type, object_id):
    """
    Delete database object by providing its type and database id.
    :return: None
    """
    with Session.begin() as session:
        db_object = session.get(object_type, object_id)
        session.delete(db_object)


def drop_rows_by_table(object_type):
    """
    Delete database table by providing its type.
    :return: None
    """
    with Session.begin() as session:
        session.query(object_type).delete()


def init_db():
    """
    DB tables initialization.
    :return: None
    """
    items_models.Base.metadata.create_all(_get_engine())
    tasks_models.Base.metadata.create_all(_get_engine())
    if not get_all_objects_by_type(Project):
        default_project = Project(**{"title": "DEFAULT", "description": "Default project."})
        create_database_object(default_project)
