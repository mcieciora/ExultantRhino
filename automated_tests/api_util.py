from os import environ
from requests import get, post
from src.postgres_sql_alchemy import get_objects_by_filters
from src.postgres_items_models import Result


def send_request(endpoint=None):
    """
    Util method to send API request.

    :return: Post response.
    """
    url = f"http://{environ['API_HOST']}:8500"
    if endpoint:
        url = f"{url}/{endpoint}"
    headers = {"Content-Type": "application/json"}
    return get(url, headers=headers)


def send_data(data):
    """
    Util method to send API request with data.

    :return: Post response.
    """
    url = f"http://{environ['API_HOST']}:8500/v1/result"
    headers = {"Content-Type": "application/json"}
    return post(url, json=data, headers=headers)


def get_result(title):
    """
    Get result objects from database by given title.

    :return: Dict with passed, failed and skipped values.
    """
    try:
        result_object = get_objects_by_filters(Result, {"title": title})[0]
    except IndexError:
        return {"info": "No object found."}
    return {value: result_object[value] for value in ["passed", "failed", "skipped"]}
