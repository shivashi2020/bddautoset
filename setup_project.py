import os

def create_directories():
    dirs = [
        'features/steps',
        'pages',
        'utils',
        'tests'
    ]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)

def create_files():
    files = {
        'config.ini': '''[settings]
capture_screenshots = true
''',
        'behave.ini': '''[behave]
default_tags = ~@skip
plugins = allure_behave.formatter:AllureFormatter
allure_report_dir = reports
''',
        'features/environment.py': '''import configparser
import allure
from selenium import webdriver

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
capture_screenshots = config.getboolean('settings', 'capture_screenshots')

def before_scenario(context, scenario):
    context.driver = webdriver.Chrome()

def after_step(context, step):
    if capture_screenshots:
        # Capture screenshot
        screenshot = context.driver.get_screenshot_as_png()
        # Attach screenshot to Allure report
        allure.attach(screenshot, name=f"Step: {step.name}", attachment_type=allure.attachment_type.PNG)

def after_scenario(context, scenario):
    context.driver.quit()
''',
        'pages/base_page.py': '''import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 10

    def find_element(self, *locator):
        return WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))

    def click(self, *locator):
        try:
            element = self.find_element(*locator)
            element.click()
            logger.info(f"Clicked on element: {locator}")
        except TimeoutException:
            logger.error(f"Element not found: {locator}")

    def enter_text(self, text, *locator):
        try:
            element = self.find_element(*locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"Entered text '{text}' into element: {locator}")
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
''',
        'pages/home_page.py': '''from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.search_box = (By.NAME, "q")
        self.search_button = (By.NAME, "btnK")

    def search(self, text):
        self.enter_text(text, *self.search_box)
        self.click(*self.search_button)
''',
        'features/example.feature': '''Feature: Search functionality
  Scenario: User searches for a keyword
    Given the user is on the home page
    When the user searches for "Selenium"
    Then the search results are displayed
''',
        'features/steps/step_definitions.py': '''import logging
from behave import given, when, then
from selenium import webdriver
from pages.home_page import HomePage
import allure

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@given('the user is on the home page')
def step_given_user_on_home_page(context):
    context.driver = webdriver.Chrome()
    context.driver.get("http://www.google.com")
    context.home_page = HomePage(context.driver)
    logger.info("User is on the home page")

@when('the user searches for "{keyword}"')
def step_when_user_searches(context, keyword):
    context.home_page.search(keyword)
    logger.info(f"User searches for '{keyword}'")

@then('the search results are displayed')
def step_then_search_results_displayed(context):
    assert "Selenium" in context.driver.title
    logger.info("Search results are displayed")
    context.driver.quit()
''',
        'requirements.txt': '''selenium
behave
pytest
allure-behave
''',
    }

    for filename, content in files.items():
        with open(filename, 'w') as f:
            f.write(content)

def main():
    create_directories()
    create_files()
    print("Project setup completed.")

if __name__ == '__main__':
    main()
