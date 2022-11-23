from pytest import mark
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


@mark.selenium
def test__check_app_content(firefox_driver):
    """
    Verifies: REQ-SEL1
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    available_tabs = {
        'Requirements': '/view_objects/requirement',
        'Test cases': '/view_objects/testcase',
        'Bugs': '/view_objects/bug',
        'Create': '/create',
    }
    for tab_name, url_value in available_tabs.items():
        firefox_driver.find_element(By.LINK_TEXT, tab_name).click()
        assert url_value in firefox_driver.current_url


@mark.selenium
def test__check_create_page_content(firefox_driver):
    """
    Verifies: REQ-SEL2
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    expected_content = ['<textarea id="description" name="description" placeholder="Insert description.."></textarea>',
                        '<input type="text" id="title" name="title" placeholder="Insert title..">',
                        '<option value="bug">Bug</option>', '<option value="testcase">TestCase</option>',
                        '<option value="requirement">Requirement</option>', '<option value="project">Project</option>',
                        '<input id="submit" type="submit" value="Submit">']
    for content in expected_content:
        assert content in firefox_driver.page_source, 'Expected elements are not in page content'


@mark.selenium
def test__create_project(firefox_driver):
    """
    Verifies: REQ-SEL2
    Verifies: REQ-SEL3
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    firefox_driver.find_element(By.NAME, 'title').send_keys('test_title')
    firefox_driver.find_element(By.NAME, 'description').send_keys('test_description')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    page_content = firefox_driver.page_source
    assert 'test_title' in firefox_driver.page_source, 'Project was not added properly'
    assert '<a href="/proj/OBJ-3">test_title</a>' in page_content, 'Project was not added properly'


@mark.selenium
def test__create_bug(firefox_driver):
    """
    Verifies: REQ-SEL3
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('Bug')
    firefox_driver.find_element(By.NAME, 'title').send_keys('test_title')
    firefox_driver.find_element(By.NAME, 'description').send_keys('test_description')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Bugs').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    assert firefox_driver.title == 'Excultant Rhino', 'Page was not loaded properly'


@mark.selenium
def test__bug_page_content(firefox_driver):
    """
    Verifies: REQ-SEL4
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_content = ['test_title', 'testcase', 'test_description', 'Template']
    firefox_driver.find_element(by=By.LINK_TEXT, value='Bugs').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    for content in expected_content:
        assert content in firefox_driver.page_source, 'Expected elements are not in page content'


@mark.selenium
def test__create_test_case(firefox_driver):
    """
    Verifies: REQ-SEL3
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('TestCase')
    firefox_driver.find_element(By.NAME, 'title').send_keys('test_title')
    firefox_driver.find_element(By.NAME, 'description').send_keys('test_description')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Test cases').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    assert firefox_driver.title == 'Excultant Rhino', 'Page was not loaded properly'


@mark.selenium
def test__tc_page_content(firefox_driver):
    """
    Verifies: REQ-SEL4
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_content = ['test_title', 'bug', 'test_description', 'Template']
    firefox_driver.find_element(by=By.LINK_TEXT, value='Test cases').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    for content in expected_content:
        assert content in firefox_driver.page_source, 'Expected elements are not in page content'


@mark.selenium
def test__create_requirement(firefox_driver):
    """
    Verifies: REQ-SEL3
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('Requirement')
    firefox_driver.find_element(By.NAME, 'title').send_keys('test_title')
    firefox_driver.find_element(By.NAME, 'description').send_keys('test_description')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Requirements').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    assert firefox_driver.title == 'Excultant Rhino', 'Page was not loaded properly'


@mark.selenium
def test__req_page_content(firefox_driver):
    """
    Verifies: REQ-SEL4
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_content = ['test_title', 'requirement', 'test_description', 'Template']
    firefox_driver.find_element(by=By.LINK_TEXT, value='Requirements').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    for content in expected_content:
        assert content in firefox_driver.page_source, 'Expected elements are not in page content'


@mark.selenium
def test__edit_object_into_different_object(firefox_driver):
    """
    Verifies: REQ-SEL5
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_data = ['<option value="bug" selected="selected">Bug</option>', '>edited_description</textarea>',
                     'value="edited_title">', '<option value="test_title" selected="selected">test_title</option>']
    firefox_driver.find_element(by=By.LINK_TEXT, value='Test cases').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='parent_project'))
    select.select_by_visible_text('test_title')
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('Bug')
    firefox_driver.find_element(by=By.ID, value='title').clear()
    firefox_driver.find_element(by=By.ID, value='title').send_keys('edited_title')
    firefox_driver.find_element(by=By.ID, value='description').clear()
    firefox_driver.find_element(by=By.ID, value='description').send_keys('edited_description')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    firefox_driver.get('http://localhost:8000/proj/OBJ-3')
    firefox_driver.find_element(by=By.LINK_TEXT, value='Bugs').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    for data in expected_data:
        assert data in firefox_driver.page_source, 'Object was not edited properly.'


@mark.selenium
def test__edit_object_into_different_object(firefox_driver):
    """
    Verifies: REQ-SEL5
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.find_element(by=By.LINK_TEXT, value='Requirements').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('Project')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    assert '<a href="/proj/OBJ-6">test_title</a>' in firefox_driver.page_source, 'Object was not edited into project'

