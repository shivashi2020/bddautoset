# features/steps/step_definitions.py

import logging
from behave import given, when, then
from selenium import webdriver
from pages.home_page import HomePage
import allure

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def attach_log(message):
    allure.attach(message, name="Log", attachment_type=allure.attachment_type.TEXT)

@given('the user is on the home page')
def step_given_user_on_home_page(context):
    context.driver = webdriver.Chrome()
    context.driver.get("http://www.google.com")
    context.home_page = HomePage(context.driver)
    message = "User is on the home page"
    logger.info(message)
    attach_log(message)

@when('the user searches for "{keyword}"')
def step_when_user_searches(context, keyword):
    context.home_page.search(keyword)
    message = f"User searches for '{keyword}'"
    logger.info(message)
    attach_log(message)

@then('the search results are displayed')
def step_then_search_results_displayed(context):
    assert "Selenium" in context.driver.title
    message = "Search results are displayed"
    logger.info(message)
    attach_log(message)
    context.driver.quit()
