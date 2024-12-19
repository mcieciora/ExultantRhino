from bottle import Bottle, response, request, run
from src.postgres_sql_alchemy import create_database_object, init_db
from src.postgres_items_models import Result

init_db()
app = Bottle()


def get_app_status():
    """
    Get streamlit app status code.

    :return: Temporary status 200.
    """
    return 200


def get_db_status():
    """
    Get database status code.

    :return: Temporary status 200.
    """
    return 200


@app.route("/", method="GET")
@app.route("/v1", method="GET")
@app.route("/v1/status", method="GET")
def status():
    """
    Return api and app versions; return api, app and db statuses.

    :return: Dict with versions and statuses.
    """
    return {
        "api_version": "0_1",
        "app_version": "0_5_1",
        "api_status": 200,
        "app_status": get_app_status(),
        "db_status": get_db_status()
    }


@app.route("/v1/result", method="POST")
def create_result():
    """
    Endpoint to create result object in database from given dict.

    :return: Dict with status.
    """
    try:
        data = request.json
        if not isinstance(data, dict):
            response.status = 400
            return {"error": "Invalid JSON data."}
        new_result = Result(**data)
        if object_creation_status := create_database_object(new_result):
            response.status = 200
            return {"shortname": object_creation_status}
    except Exception as e:
        response.status = 500
        return {"error": str(e)}


run(app, host="0.0.0.0", port=8500)
