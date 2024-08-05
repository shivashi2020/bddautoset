# features/environment.py

import configparser
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
