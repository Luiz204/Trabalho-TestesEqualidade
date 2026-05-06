from selenium.webdriver.common.by import By
from web_tests.pages.base_page import BasePage

class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"
    _USERNAME  = (By.ID, "user-name")
    _PASSWORD  = (By.ID, "password")
    _LOGIN_BTN = (By.ID, "login-button")
    _ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.driver.get(self.URL)
        return self

    def login(self, username, password):
        self._type(self._USERNAME, username)
        self._type(self._PASSWORD, password)
        self._click(self._LOGIN_BTN)
        return self

    def get_error_message(self):
        return self._text(self._ERROR_MSG)

    def is_error_visible(self):
        return self._is_visible(self._ERROR_MSG)