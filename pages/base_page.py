# pages/base_page.py

import logging
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def attach_log(self, message):
        allure.attach(message, name="Log", attachment_type=allure.attachment_type.TEXT)

    def find_element(self, *locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def click(self, *locator):
        try:
            element = self.find_element(*locator)
            element.click()
            message = f"Clicked on element: {locator}"
            logger.info(message)
            self.attach_log(message)
        except TimeoutException:
            message = f"Element not found: {locator}"
            logger.error(message)
            self.attach_log(message)

    def enter_text(self, text, *locator):
        try:
            element = self.find_element(*locator)
            element.clear()
            element.send_keys(text)
            message = f"Entered text '{text}' into element: {locator}"
            logger.info(message)
            self.attach_log(message)
        except TimeoutException:
            message = f"Element not found: {locator}"
            logger.error(message)
            self.attach_log(message)
