from pytest import mark
from src.main import get_itfoss_com_status_code


@mark.nightly
def test__nightly__get_itfoss_com_status_code(expected_status_code):
    return_status_code = get_itfoss_com_status_code()
    assert return_status_code == expected_status_code, f"Status code check failed. " \
                                                       f"Actual {return_status_code}, Expected: {expected_status_code}"
