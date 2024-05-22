from os import environ
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

STANDARD_WAIT = 0.5
LOAD_WAIT = 1


class SeleniumUtil:
    def __init__(self):
        options = Options()
        options.add_argument("-headless")
        self.driver = webdriver.Firefox(options=options)
        self.api_url = f"http://{environ['API_HOST']}:8501"
        self.driver.get(self.api_url)
        sleep(LOAD_WAIT)

    def find_element_by_link_text(self, link_text):
        return self.driver.find_element(By.LINK_TEXT, link_text)

    def find_element_by_xpath_accessible_text(self, accessible_text, xpath_element="aria-label"):
        return self.driver.find_element(By.XPATH, f"//*[@{xpath_element}='{accessible_text}']")

    def submit_form(self):
        submit_button = self.driver.find_element(By.XPATH, f"//button[@kind='secondary']")
        submit_button.click()
        sleep(LOAD_WAIT)

    def write_input(self, accessible_text, text):
        input_object = self.find_element_by_xpath_accessible_text(accessible_text)
        input_object.send_keys(text)
        sleep(STANDARD_WAIT)

    def overwrite_value(self, accessible_text, text):
        input_object = self.find_element_by_xpath_accessible_text(accessible_text)
        input_object.clear()
        sleep(STANDARD_WAIT)
        input_object.send_keys(text)
        sleep(STANDARD_WAIT)

    def choose_from_select_box(self, accessible_text, select_item_text):
        select_box = self.find_element_by_xpath_accessible_text(accessible_text)
        select_box.send_keys(select_item_text)
        sleep(STANDARD_WAIT)
        select_box.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
        select_box.send_keys()
        sleep(STANDARD_WAIT)

    def choose_from_search_box(self, accessible_text, select_item_text):
        select_box = self.find_element_by_xpath_accessible_text(accessible_text, xpath_element="title")
        select_box.click()
        select_box.send_keys(select_item_text)
        sleep(STANDARD_WAIT)
        select_box.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
        sleep(STANDARD_WAIT)

    def click_link_text(self, page_name):
        self.find_element_by_link_text(page_name).click()
        sleep(STANDARD_WAIT)

    def go_to_page(self, url):
        self.driver.get(url)
        sleep(LOAD_WAIT)

    def terminate(self):
        self.driver.close()
