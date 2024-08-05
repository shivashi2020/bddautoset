from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.search_box = (By.NAME, "q")
        self.search_button = (By.XPATH, "(//input[@name='btnK'])[2]")

    def search(self, text):
        self.enter_text(text, *self.search_box)
        self.click(*self.search_button)
