from pytest import fixture


@fixture
def expected_status_code():
    """
    Return status 200 for test purpose.

    :return: 200
    """
    yield 200
