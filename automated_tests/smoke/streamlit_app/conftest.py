from pytest import fixture
from automated_tests.selenium_util import SeleniumUtil


@fixture(scope="function")
def selenium_util():
    """
    Fixture opens browser window with exultant rhino app.
    :return: Yielding browser app.
    """
    selenium_util = SeleniumUtil()
    yield selenium_util
    selenium_util.terminate()
