from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.postgres_models import Base, Bug, Project, Release, Requirement, TestCase


def _get_engine():
    """
    Get engine object with connection arguments taken from environment
    :return: Engine class object.
    """
    return create_engine(f"postgresql://{environ['POSTGRES_USER']}:{environ['POSTGRES_PASSWORD']}@"
                         f"{environ['HOST_NAME']}:{environ['DB_PORT']}/{environ['POSTGRES_DB']}")


def get_session():
    """
    Generate session with current engine class object value
    :return: Session class object.
    """
    session_maker = sessionmaker(bind=_get_engine())
    _get_session = session_maker()
    return _get_session


def convert_to_dict(database_object):
    """
    Create dict out of given database object
    :param database_object:
    :return:
    """
    return {column.name: getattr(database_object, column.name) for column in database_object.__table__.columns}


def get_next_shortname(object_type):
    """
    Get next object shortname value based on given object type
    :param object_type: Any of Project, Release, Requirement, TestCase, Bug.
    :return: String value in (proj/rls/req/tc/bug)-xxx format.
    """
    # TODO cover with smoke tests
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
    # TODO cover with smoke tests
    return get_session().query(object_type).filter_by(shortname=shortname).first()


def get_all_objects_by_type(object_type):
    """
    Get list of database objects by their type (Project, Release, Requirement, TestCase, Bug)
    :return: List of database objects.
    """
    # TODO cover with smoke tests
    return [convert_to_dict(db_object) for db_object in get_session().query(object_type).all()]


def get_objects_by_filters(object_type, filters_dict):
    """
    Get list of database objects by their type (Project, Release, Requirement, TestCase, Bug)
    and filtered by given query.
    :return: List of database objects.
    """
    # TODO cover with smoke tests
    query = get_session().query(object_type)
    for key, value in filters_dict.items():
        query = query.filter(getattr(object_type, key).like("%%%s%%" % value)).all()
    return [convert_to_dict(db_object) for db_object in query]


def create_database_object(object_to_commit):
    """
    Create database object from given dictionary
    :param object_to_commit: Object dictionary.
    :return: Committed object shortname value.
    """
    # TODO cover with smoke tests
    setattr(object_to_commit, "shortname", get_next_shortname(type(object_to_commit)))
    get_session().add(object_to_commit)
    get_session().commit()
    return object_to_commit.shortname


def edit_database_object(object_type, object_id, new_data):
    # TODO add description
    # TODO cover with smoke tests
    db_object = get_session().get(object_type, object_id)
    for key, value in new_data.items():
        setattr(db_object, key, value)
    get_session().commit()


def delete_database_object(object_type, object_id):
    # TODO add description
    # TODO cover with smoke tests
    db_object = get_session().get(object_type, object_id)
    get_session().delete(db_object)
    get_session().commit()


def drop_rows_by_table(object_type):
    # TODO add description
    # TODO cover with smoke tests
    get_session().query(object_type).delete()
    get_session().commit()


if __name__ == '__main__':
    Base.metadata.create_all(_get_engine())
