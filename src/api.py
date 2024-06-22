from json import dumps
from bottle import response, request, route, run
from src.postgres_sql_alchemy import (
    Bug,
    create_database_object,
    get_all_objects_by_type,
    get_database_object,
    get_objects_by_filters,
    Project,
    Release,
    Requirement,
    TestCase,
)

object_type_map = {
    "project": Project,
    "release": Release,
    "requirement": Requirement,
    "testcase": TestCase,
    "bug": Bug,
}


def return_response(return_table):
    """
    Serialize database objects list to JSON formatted string.

    :return: JSON formatted string.
    """
    response.content_type = "application/json"
    return dumps(return_table)


@route("/status")
def status():
    """
    Get current Streamlit application, API daemon and database statuses.

    :return: JSON formatted string.
    """
    # TODO implement app, api and db statuses check
    return return_response([{"app_status": 200, "api_status": 200, "db_status": 200}])


@route("/get/<object_type>/<shortname>")
def get_object_by_shortname(object_type, shortname):
    """
    Get database object by its type and shortname.

    :return: JSON formatted string.
    """
    return_value = get_database_object(object_type_map[object_type], shortname)
    return return_response(return_value)


@route("/get/<object_type>")
def get_objects(object_type):
    """
    Get list of database objects by their type (Project, Release, Requirement, TestCase, Bug).

    Additional filters may be added as query parameters in API call.
    See: request_map dictionary values or call /help/objects

    :return: JSON formatted string.
    """
    if parameters := dict(request.params.items()):
        return_value = get_objects_by_filters(object_type_map[object_type], parameters)
    else:
        return_value = get_all_objects_by_type(object_type_map[object_type])
    return return_response(return_value)


@route("/insert/<object_type>")
def insert(object_type):
    """
    Insert object into database with given parameters values passed as query.

    :return: Committed object shortname value.
    """
    model_object = object_type_map[object_type]
    new_object = model_object()
    model_columns = [column.name for column in model_object.__table__.columns]
    for key, value in request.params.items():
        if key in model_columns:
            setattr(new_object, key, value)
    return return_response({"committed_shortname": create_database_object(new_object)})


if __name__ == "__main__":
    run(host="0.0.0.0", port=8101)
