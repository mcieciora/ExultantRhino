from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.postgres_models import Base, Bug, Project, Release, Requirement, TestCase


def _get_engine():
    """
    Get engine object with connection arguments taken from environment.
    :return: Engine class object.
    """
    return create_engine(f"postgresql://{environ['POSTGRES_USER']}:{environ['POSTGRES_PASSWORD']}@"
                         f"{environ['HOST_NAME']}:{environ['DB_PORT']}/{environ['POSTGRES_DB']}")


def get_session():
    """
    Generate session with current engine class object value.
    :return: Session class object.
    """
    session_maker = sessionmaker(bind=_get_engine())
    _get_session = session_maker()
    return _get_session


def convert_to_dict(database_object):
    """
    Create dict out of given database object.
    :return: Database object dict.
    """
    try:
        return {column.name: getattr(database_object, column.name) for column in database_object.__table__.columns}
    except AttributeError:
        return {}


def get_next_shortname(object_type):
    """
    Get next object shortname value based on given object type.
    :return: String value in (proj/rls/req/tc/bug)-xxx format.
    """
    shortname_prefix = {Project: "proj", Release: "rls", Requirement: "req", TestCase: "tc", Bug: "bug"}
    try:
        last_object = get_all_objects_by_type(object_type)[-1]
        last_object_id = int(last_object["shortname"].split("-")[1])
        return f"{shortname_prefix[object_type]}-{last_object_id + 1}"
    except IndexError:
        return f"{shortname_prefix[object_type]}-0"


def get_database_object(object_type, shortname):
    """
    Get database object by its type (Project, Release, Requirement, TestCase, Bug) and shortname
    in (proj/rls/req/tc/bug)-xxx format.
    :return: Database object.
    """
    database_object = get_session().query(object_type).filter_by(shortname=shortname).first()
    return convert_to_dict(database_object)


def get_all_objects_by_type(object_type):
    """
    Get list of database objects by their type (Project, Release, Requirement, TestCase, Bug).
    :return: List of database objects.
    """
    return [convert_to_dict(db_object) for db_object in get_session().query(object_type).all()]


def get_objects_by_filters(object_type, filters_dict):
    """
    Get list of database objects by their type (Project, Release, Requirement, TestCase, Bug)
    and filtered by given query.
    :return: List of database objects.
    """
    query = get_session().query(object_type)
    for key, value in filters_dict.items():
        query = query.filter(getattr(object_type, key).like("%%%s%%" % value)).all()
    return [convert_to_dict(db_object) for db_object in query]


def create_database_object(object_to_commit):
    """
    Create database object from given dictionary.
    :return: Committed object shortname value.
    """
    setattr(object_to_commit, "shortname", get_next_shortname(type(object_to_commit)))
    session = get_session()
    session.add(object_to_commit)
    session.commit()
    return object_to_commit.shortname


def edit_database_object(object_type, object_id, new_data):
    """
    Edit database object by providing new values' dict.
    :return: None
    """
    session = get_session()
    db_object = session.get(object_type, object_id)
    for key, value in new_data.items():
        setattr(db_object, key, value)
    session.commit()


def delete_database_object(object_type, object_id):
    """
    Delete database object by providing its type and database id.
    :return: None
    """
    session = get_session()
    db_object = session.get(object_type, object_id)
    session.delete(db_object)
    session.commit()


def drop_rows_by_table(object_type):
    """
    Delete database table by providing its type.
    :return: None
    """
    session = get_session()
    session.query(object_type).delete()
    session.commit()


def init_db():
    """
    DB tables initialization.
    :return: None
    """
    Base.metadata.create_all(_get_engine())
