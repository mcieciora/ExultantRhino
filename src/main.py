from requests import get


def get_google_com_status_code():
    """
    Get https://google.com status code.

    :return: Status code
    """
    return get(url="https://google.com", timeout=5).status_code
