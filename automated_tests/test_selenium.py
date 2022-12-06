from json import dumps
from time import sleep
from pytest import mark
from requests import post
from selenium.webdriver.common.keys import Keys
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
        assert url_value in firefox_driver.current_url, f'Expected: {url_value} Actual: {firefox_driver.current_url}'


@mark.selenium
def test__check_create_page_content(firefox_driver):
    """
    Verifies: REQ-SEL2
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    expected_content = ['<textarea id="description" name="description" placeholder="Insert description.."></textarea>',
                        '<input type="text" id="title" name="title" placeholder="Insert title.." required="">',
                        '<input type="text" id="parent" name="parent" placeholder="Search objects..">',
                        '<option value="bug">Bug</option>', '<option value="testcase">TestCase</option>',
                        '<option value="requirement">Requirement</option>', '<option value="project">Project</option>',
                        '<input id="submit" type="submit" value="Submit">']
    for content in expected_content:
        assert content in firefox_driver.page_source, f'Expected: {content} Actual: {firefox_driver.page_source}'


@mark.selenium
def test__create_project(firefox_driver):
    """
    Verifies: REQ-SEL2
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_content = ['<a href="/proj/OBJ-59">test_title</a>',
                        '<strong>Info</strong> test_title was successfully created.']
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    firefox_driver.find_element(By.NAME, 'title').send_keys('test_title')
    firefox_driver.find_element(By.NAME, 'description').send_keys('test_description')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    for content in expected_content:
        assert content in firefox_driver.page_source, f'Expected: {content} Actual: {firefox_driver.page_source}'


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
    assert '<strong>Info</strong> test_title was successfully created.' in firefox_driver.page_source, \
        f'Expected: <strong>Info</strong> test_title was successfully created. Actual: {firefox_driver.page_source}'


@mark.selenium
def test__tc_page_content(firefox_driver):
    """
    Verifies: REQ-SEL4
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_content = ['value="test_title" required="">', 'name="description">test_description</textarea>',
                        '<option value="testcase" selected="selected">TestCase</option>',
                        '<option value="new_proj" selected="selected">new_proj</option>']
    firefox_driver.get('http://localhost:8000/edit/OBJ-60')
    for content in expected_content:
        assert content in firefox_driver.page_source, f'Expected: {content} Actual: {firefox_driver.page_source}'


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
    autocomplete_object = firefox_driver.find_element(By.NAME, 'parent')
    autocomplete_object.send_keys('oBj-60')
    autocomplete_object.send_keys(Keys.ARROW_DOWN)
    autocomplete_object.send_keys(Keys.RETURN)
    firefox_driver.find_element(by=By.ID, value='submit').click()
    assert '<strong>Info</strong> test_title was successfully created.' in firefox_driver.page_source, \
        f'Expected: <strong>Info</strong> test_title was successfully created. Actual: {firefox_driver.page_source}'


@mark.selenium
def test__bug_page_content(firefox_driver):
    """
    Verifies: REQ-SEL4
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_content = ['value="test_title" required="">', 'name="description">test_description</textarea>',
                        'value="OBJ-60: test_title">', '<option value="bug" selected="selected">Bug</option>',
                        '<option value="new_proj" selected="selected">new_proj</option>']
    firefox_driver.get('http://localhost:8000/edit/OBJ-61')
    for content in expected_content:
        assert content in firefox_driver.page_source, f'Expected: {content} Actual: {firefox_driver.page_source}'


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
    assert '<strong>Info</strong> test_title was successfully created.' in firefox_driver.page_source, \
        f'Expected: <strong>Info</strong> test_title was successfully created. Actual: {firefox_driver.page_source}'


@mark.selenium
def test__req_page_content(firefox_driver):
    """
    Verifies: REQ-SEL4
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_content = ['value="test_title" required="">', 'name="description">test_description</textarea>',
                        '<option value="requirement" selected="selected">Requirement</option>',
                        '<option value="new_proj" selected="selected">new_proj</option>']
    firefox_driver.get('http://localhost:8000/edit/OBJ-62')
    for content in expected_content:
        assert content in firefox_driver.page_source, f'Expected: {content} Actual: {firefox_driver.page_source}'


@mark.selenium
def test__edit_object_into_different_object(firefox_driver):
    """
    Verifies: REQ-SEL5
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_data = ['<option value="bug" selected="selected">Bug</option>', '>edited_description</textarea>',
                     'value="edited_title" required="">', '<option value="test_title" selected="selected">test_title'
                                                          '</option>',
                     '<input type="text" id="parent" name="parent" value="OBJ-1: new_proj">']
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
    autocomplete_object = firefox_driver.find_element(By.NAME, 'parent')
    autocomplete_object.clear()
    autocomplete_object.send_keys('oBj-')
    autocomplete_object.send_keys(Keys.ARROW_DOWN)
    autocomplete_object.send_keys(Keys.ARROW_DOWN)
    autocomplete_object.send_keys(Keys.RETURN)
    firefox_driver.find_element(by=By.ID, value='submit').click()
    firefox_driver.get('http://localhost:8000/proj/OBJ-59')
    firefox_driver.find_element(by=By.LINK_TEXT, value='Bugs').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    for data in expected_data:
        assert data in firefox_driver.page_source, f'Object {data} was not edited properly.'


@mark.selenium
def test__edit_object_into_project(firefox_driver):
    """
    Verifies: REQ-SEL5
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_data = ['<strong>Info</strong> edited_title was successfully edited.',
                     '<a href="/proj/OBJ-53">edited_title</a>']
    firefox_driver.find_element(by=By.LINK_TEXT, value='Bugs').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Edit').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('Project')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    for content in expected_data:
        assert content in firefox_driver.page_source, f'Expected: {content} Actual: {firefox_driver.page_source}'


@mark.selenium
def test__delete_object(firefox_driver):
    """
    Verifies: REQ-SEL3
    Verifies: REQ-SEL6
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('TestCase')
    firefox_driver.find_element(By.NAME, 'title').send_keys('object_to_delete')
    firefox_driver.find_element(By.NAME, 'description').send_keys('test_object_to_delete')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Test cases').click()
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Delete').click()
    assert '<strong>Info</strong> OBJ-63 was successfully deleted.' in firefox_driver.page_source, \
        f'Expected: <strong>Info</strong> OBJ-63 was successfully deleted. Actual: {firefox_driver.page_source}'
    firefox_driver.find_element(by=By.LINK_TEXT, value='Test cases').click()
    assert 'object_to_delete' not in firefox_driver.page_source, \
        f'Expected: object_to_delete Actual: {firefox_driver.page_source}'


@mark.selenium
def test__check_dependencies(firefox_driver):
    """
    Verifies: REQ-SEL7
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_data = ['<a href="/edit/OBJ-64" target="_blank" rel="noopener noreferrer">OBJ-64: test_case_title</a>',
                     '<p>Depends on: <a href="/edit/OBJ-0" target="_blank" rel="noopener noreferrer">OBJ-0: '
                     'Template</a></p>', '<a class="edit" href="/edit/OBJ-63">Edit</a>',
                     '<a class="delete" href="/delete/OBJ-63">Delete</a>']
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('Requirement')
    firefox_driver.find_element(By.NAME, 'title').send_keys('test_req_title')
    firefox_driver.find_element(By.NAME, 'description').send_keys('test_req_description')
    autocomplete_object = firefox_driver.find_element(By.NAME, 'parent')
    autocomplete_object.send_keys('oBj-')
    autocomplete_object.send_keys(Keys.ARROW_DOWN)
    autocomplete_object.send_keys(Keys.RETURN)
    firefox_driver.find_element(by=By.ID, value='submit').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('TestCase')
    firefox_driver.find_element(By.NAME, 'title').send_keys('test_case_title')
    firefox_driver.find_element(By.NAME, 'description').send_keys('test_case_description')
    autocomplete_object = firefox_driver.find_element(By.NAME, 'parent')
    autocomplete_object.send_keys('test_req_title')
    autocomplete_object.send_keys(Keys.ARROW_DOWN)
    autocomplete_object.send_keys(Keys.RETURN)
    firefox_driver.find_element(by=By.ID, value='submit').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Requirements').click()
    for data in expected_data:
        assert data in firefox_driver.page_source, f'Expected: {data} Actual: {firefox_driver.page_source}'


@mark.selenium
def test__dashboard_content(firefox_driver):
    """
    Verifies: REQ-SEL8
    Verifies: REQ-SEL9
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_data = ['<h1>1</h1>', '<h1>3</h1>', '<h1>4</h1>', '>OBJ-60: test_title</button>',
                     '>OBJ-52: req_3</button>', '>OBJ-62: test_title</button>', '1 active bugs:</h4>',
                     ' <h4>There are 2 requirements', '<h2>test_name_1</h2>']
    firefox_driver.get('http://localhost:8000/proj/OBJ-1')
    for content in expected_data:
        assert content in expected_data, f'Expected: {content} Actual: {firefox_driver.page_source}'
    firefox_driver.get('http://localhost:8000/delete/OBJ-60')
    firefox_driver.get('http://localhost:8000/delete/OBJ-52')
    firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
    select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
    select.select_by_visible_text('TestCase')
    firefox_driver.find_element(By.NAME, 'title').send_keys('test_title')
    firefox_driver.find_element(By.NAME, 'description').send_keys('test_description')
    autocomplete_object = firefox_driver.find_element(By.NAME, 'parent')
    autocomplete_object.send_keys('OBJ-62')
    autocomplete_object.send_keys(Keys.ARROW_DOWN)
    autocomplete_object.send_keys(Keys.RETURN)
    firefox_driver.find_element(by=By.ID, value='submit').click()
    expected_data = ['<h1>0</h1>', '<h1>4</h1>', '<h1>3</h1>', '<h4>There are no active bugs.</h4>',
                     '<h4>All requirements are covered with test cases</h4>']
    for content in expected_data:
        assert content in expected_data, f'Expected: {content} Actual: {firefox_driver.page_source}'


@mark.selenium
def test__requirements_tab_content(firefox_driver):
    """
    Verifies: REQ-SEL9
    Verifies: REQ-SEL10
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_data = ['OBJ-56: test_name_1', 'OBJ-57: test_name_2', 'OBJ-58: test_name_3', 'OBJ-50 OBJ-53 pass',
                     'OBJ-50 OBJ-54 fail', 'OBJ-51 OBJ-55 not_run']
    firefox_driver.get('http://localhost:8000/proj/OBJ-1')
    firefox_driver.find_element(by=By.LINK_TEXT, value='Releases').click()
    for content in expected_data:
        assert content in expected_data, f'Expected: {content} Actual: {firefox_driver.page_source}'
    firefox_driver.find_element(by=By.ID, value='collapsible').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Delete').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Requirements').click()
    assert 'OBJ-56: test_name_1' not in firefox_driver.page_source, f'Expected: OBJ-56: test_name_1 ' \
                                                                    f'Actual: {firefox_driver.page_source}'


@mark.selenium
def test__add_requirement_and_check_release_dashboard(firefox_driver):
    """
    Verifies: REQ-SEL10
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    url = "http://localhost:8000/upload"
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    post(url, data=dumps({
        'project_name': 'new_proj', 'release_name': 'test_name_4', 'reqs': {
            'OBJ-51': {'OBJ-55': 'pass'},
            'OBJ-62': {'OBJ-65': 'pass'},
        }
    }), headers=headers, timeout=5)
    firefox_driver.get('http://localhost:8000/proj/OBJ-1')
    expected_data = ['test_name_4', "{'fail': 0, 'pass': 2, 'not_run': 0}"]
    for content in expected_data:
        assert content in expected_data, f'Expected: {content} Actual: {firefox_driver.page_source}'


@mark.selenium
def test__release_dashboard_screenshot(firefox_driver):
    """
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    sleep(1)
    firefox_driver.save_screenshot('test__release_dashboard_screenshot.png')


@mark.selenium
def test__test_case_has_bug_badge(firefox_driver):
    """
    Verifies: REQ-SEL11
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.get('http://127.0.0.1:8000/edit/OBJ-61')
    firefox_driver.find_element(by=By.NAME, value='parent').clear()
    autocomplete_object = firefox_driver.find_element(By.NAME, 'parent')
    autocomplete_object.send_keys('OBJ-65')
    autocomplete_object.send_keys(Keys.ARROW_DOWN)
    autocomplete_object.send_keys(Keys.RETURN)
    firefox_driver.find_element(by=By.ID, value='submit').click()
    firefox_driver.find_element(by=By.LINK_TEXT, value='Test cases').click()
    assert 'OBJ-65: test_title<span class="badge">Bug</span>' in firefox_driver.page_source, \
        f'Expected: OBJ-65: test_title<span class="badge">Bug</span> Actual: {firefox_driver.page_source}'


@mark.selenium
def test__validate_corresponding_object_types(firefox_driver):
    """
    Verifies: REQ-SEL12
    Verifies: REQ-SEL13
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    corresponding_parent_types = {'Bug': 'TestCase',
                                  'TestCase': 'Requirement',
                                  'Requirement': 'Project',
                                  'Project': 'Project'}
    test_data = ['Project', 'Bug', 'TestCase', 'Requirement']

    for element in test_data:
        firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
        firefox_driver.find_element(By.NAME, 'title').send_keys(f'test_{element}')
        firefox_driver.find_element(By.NAME, 'description').send_keys('test_description')
        select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
        select.select_by_visible_text(element)
        firefox_driver.find_element(by=By.ID, value='submit').click()
        success_response = f'<strong>Info</strong> test_{element} was successfully created.'
        assert success_response in firefox_driver.page_source, f'Expected: {success_response} Actual: ' \
                                                               f'{firefox_driver.page_source}'

    for object_type, parent_type in corresponding_parent_types.items():
        for element in test_data:
            firefox_driver.find_element(by=By.LINK_TEXT, value='Create').click()
            firefox_driver.find_element(By.NAME, 'title').send_keys(f'{object_type}-{element}')
            firefox_driver.find_element(By.NAME, 'description').send_keys('test_description')
            select = Select(firefox_driver.find_element(by=By.ID, value='object_type'))
            select.select_by_visible_text(object_type)
            autocomplete_object = firefox_driver.find_element(By.NAME, 'parent')
            autocomplete_object.send_keys(f'test_{element}')
            autocomplete_object.send_keys(Keys.ARROW_DOWN)
            autocomplete_object.send_keys(Keys.RETURN)
            firefox_driver.find_element(by=By.ID, value='submit').click()
            response = f'<strong>Info</strong> {object_type.lower()} shall be assigned to ' \
                       f'{parent_type.lower()}'
            if element == parent_type:
                response = f'<strong>Info</strong> {object_type}-{element} was successfully created.'
            assert response in firefox_driver.page_source, f'Expected: {response} Actual: ' \
                                                           f'{firefox_driver.page_source}'


@mark.selenium
def test__delete_template_project(firefox_driver):
    """
    Verifies: REQ-SEL14
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_message = 'Base project: Template cannot be deleted.'
    firefox_driver.find_element(By.NAME, 'project_name').send_keys('Template')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    assert expected_message in firefox_driver.page_source, f'Expected: {expected_message} Actual: ' \
                                                           f'{firefox_driver.page_source}'


@mark.selenium
def test__delete_non_existing_project(firefox_driver):
    """
    Verifies: REQ-SEL14
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    expected_message = 'No such project name.'
    firefox_driver.find_element(By.NAME, 'project_name').send_keys('non_existing_project')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    assert expected_message in firefox_driver.page_source, f'Expected: {expected_message} Actual: ' \
                                                           f'{firefox_driver.page_source}'


@mark.selenium
def test__delete_project(firefox_driver):
    """
    Verifies: REQ-SEL14
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.find_element(By.NAME, 'project_name').send_keys('new_proj')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    assert '>new_proj</a>' not in firefox_driver.page_source, f'Expected: >new_proj</a> Actual: ' \
                                                              f'{firefox_driver.page_source}'


@mark.selenium
def test__delete_current_project(firefox_driver):
    """
    Verifies: REQ-SEL14
    :param firefox_driver: Firefox webdriver; taken from fixture
    :return: None
    """
    firefox_driver.get('http://localhost:8000/proj/OBJ-59')
    firefox_driver.find_element(By.NAME, 'project_name').send_keys('test_title')
    firefox_driver.find_element(by=By.ID, value='submit').click()
    number_or_occurrences = firefox_driver.page_source.count('>Template')
    assert number_or_occurrences == 2, f'Expected: 2 Actual: {number_or_occurrences}'
