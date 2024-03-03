from bottle import FormsDict, response, request, route, run
from json import dumps
from src.postgres_sql_alchemy import Bug, create_database_object, get_all_objects_by_type, \
    get_database_object, get_objects_by_filters, Project, Release, Requirement, TestCase


requests_map = {
    "status": {"description": "Get status of Streamlit app, API and database.",
               "format": "/status"},
    "get_help": {"description": "Show help page.",
                 "format": "/get_help or /get_help/<request_name>",
                 "request_name_value": "Any request name eg. get_object"},
    "get_object": {"description": "Get object by type and id",
                   "format": "/get_object/<object_type>/<shortname>",
                   "object_type_value": "'project', 'release', 'requirement', 'testcase', 'bug'",
                   "shortname_value": "Object shortname. eg. proj-0"},
    "get_objects": {"description": "Get object by given filter.",
                    "format": "/get_objects/<object_type>?<filters> eg. /get_object/release?name=new+release "
                              "(plus signs are replaced by spaces)",
                    "object_type_value": "'project', 'release', 'requirement', 'testcase', 'bug'",
                    "filters_value": {
                        "id": "Object database id.",
                        "shortname": "Given database object shortname in (proj/rls/req/tc/bug)-xxx format.",
                        "title": "Title of the object.",
                        "description": "Object description.",
                        "project_id": "Parent project id in proj-xxx format.",
                        "parent": "Parent object in (proj/rls/req/tc/bug)-xxx format."
                    }
                    },
    "insert_object": {"description": "Insert an object with given parameters.",
                      "format": "/insert_object/<object_type>?<parameters> eg. "
                                "/insert_object/release?title=new+release (plus signs are replaced by spaces)",
                      "object_type_value": "'project', 'release', 'requirement', 'testcase', 'bug'",
                      "parameters_value": {"title": "(Required) Name of the object",
                                           "description": "(Required) Description of the object",
                                           "project_id": "(Required) Set parent project that the object belongs to. "
                                                         "Not applicable to projects.",
                                           "parent": "(Required) Set parent of this object. Not applicable to projects."
                                           }
                      }
}

object_type_map = {
    "project": Project,
    "release": Release,
    "requirement": Requirement,
    "testcase": TestCase,
    "bug": Bug
}


def return_response(return_table):
    """
    Serialize database objects list to JSON formatted string
    :param return_table: database objects list.
    :return: JSON formatted string.
    """
    response.content_type = 'application/json'
    return dumps(return_table)


@route("/status")
def status():
    """
    Get current Streamlit application, API daemon and database statuses
    :return: JSON formatted string.
    """
    # TODO implement app, api and db statuses check
    return return_response([{"app_status": 200, "api_status": 200, "db_status": 200}])


@route("/get_help")
def get_help():
    """
    Get list of all endpoints with description, format and additional pieces of information
    :return: JSON formatted string.
    """
    return return_response(requests_map)


@route("/get_help/<request_name>")
def get_help_by_request(request_name):
    """
    Get description, format and additional pieces of information of endpoint by its name
    :return: JSON formatted string.
    """
    return return_response(requests_map[request_name])


@route("/get_object/<object_type>/<shortname>")
def get_object(object_type, shortname):
    """
    Get database object by its type (Project, Release, Requirement, TestCase, Bug) and shortname
    in (proj/rls/req/tc/bug)-xxx format.
    :return: JSON formatted string.
    """
    # TODO write smoke tests
    return_value = get_database_object(object_type_map[object_type], shortname)
    return return_response(return_value)


@route("/get_objects/<object_type>")
def get_objects(object_type):
    """
    Get list of database objects by their type (Project, Release, Requirement, TestCase, Bug)
    Additional filters may be added as query parameters in API call.
    See: request_map dictionary values or call /get_help/get_objects
    :return: JSON formatted string.
    """
    # TODO write smoke tests
    if type(params := request.params) is FormsDict:
        filters = {x: y for x, y in params.items()}
        return_value = get_objects_by_filters(object_type_map[object_type], filters)
    else:
        return_value = get_all_objects_by_type(object_type_map[object_type])
    return return_response(return_value)


@route("/insert_object/<object_type>")
def insert_object(object_type):
    """
    Insert object into database with given parameters values passed as query.
    :return: Committed object shortname value.
    """
    # TODO write smoke tests
    model_object = object_type_map[object_type]
    new_object = model_object()
    model_columns = [column.name for column in model_object.__table__.columns]
    for key, value in request.params.items():
        if key in model_columns:
            setattr(new_object, key, value)
    return return_response({"committed_shortname": create_database_object(new_object)})


if __name__ == '__main__':
    run(host="0.0.0.0", port=8101)
