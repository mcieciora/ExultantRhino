from os import environ
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

STANDARD_WAIT = 0.5
LOAD_WAIT = 1


class SeleniumUtil:
    """Selenium utilization class."""
    def __init__(self):
        options = Options()
        options.add_argument("-headless")
        service = Service(executable_path="./automated_tests/utils/geckodriver/geckodriver_0_34_0")
        self.driver = webdriver.Firefox(service=service, options=options)
        self.api_url = f"http://{environ['API_HOST']}:8501"
        self.driver.get(self.api_url)
        sleep(LOAD_WAIT)

    def find_element_by_link_text(self, link_text):
        """
        Find page element by given link text.

        :return: Page element.
        """
        return self.driver.find_element(By.LINK_TEXT, link_text)

    def find_element_by_xpath_accessible_text(self, accessible_text, xpath_element="aria-label"):
        """
        Find page element by given accessible text and optional xpath element name.

        :return: Page element.
        """
        return self.driver.find_element(By.XPATH, f"//*[@{xpath_element}='{accessible_text}']")

    def find_elements_by_xpath_accessible_text(self, accessible_text, xpath_element="aria-label"):
        """
        Find page elements by given accessible text and optional xpath element name.

        :return: Page elements.
        """
        return self.driver.find_elements(By.XPATH, f"//*[@{xpath_element}='{accessible_text}']")

    def get_xpath_text_value(self, accessible_text, xpath_element):
        """
        Get page elements text by given accessible text and optional xpath element name.

        :return: Page element.
        """
        return self.find_element_by_xpath_accessible_text(accessible_text, xpath_element).text

    def submit_form(self):
        """Submit secondary form in page."""
        submit_button = self.driver.find_element(By.XPATH, "//button[@kind='secondary']")
        submit_button.click()
        sleep(LOAD_WAIT)

    def submit_form_by_text(self, button_text):
        """Find secondary form by button text and submit."""
        submit_buttons = self.driver.find_elements(By.XPATH, "//button[@kind='secondary']")
        submit_button = [button for button in submit_buttons if button.text == button_text]
        submit_button[0].click()
        sleep(LOAD_WAIT)

    def write_input(self, accessible_text, text):
        """Insert value into found element."""
        input_object = self.find_element_by_xpath_accessible_text(accessible_text)
        input_object.send_keys(text)
        sleep(STANDARD_WAIT)

    def overwrite_value(self, accessible_text, text):
        """Remove value from found element and insert new value."""
        input_object = self.find_element_by_xpath_accessible_text(accessible_text)
        input_object.clear()
        sleep(STANDARD_WAIT)
        input_object.send_keys(text)
        sleep(STANDARD_WAIT)

    def choose_from_select_box(self, accessible_text, select_item_text):
        """Find given value in select box and choose it."""
        select_box = self.find_element_by_xpath_accessible_text(accessible_text)
        select_box.send_keys(select_item_text)
        sleep(STANDARD_WAIT)
        select_box.send_keys(Keys.ARROW_DOWN, Keys.RETURN)
        sleep(STANDARD_WAIT)

    def click_link_text(self, page_name):
        """Find element by given name and click it."""
        self.find_element_by_link_text(page_name).click()
        sleep(STANDARD_WAIT)

    def go_to_page(self, url):
        """Go to given url page."""
        self.driver.get(url)
        sleep(LOAD_WAIT)

    def terminate(self):
        """Close selenium driver."""
        self.driver.close()
