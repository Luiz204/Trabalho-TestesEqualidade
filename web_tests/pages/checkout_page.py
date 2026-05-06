from selenium.webdriver.common.by import By
from web_tests.pages.base_page import BasePage

class CheckoutPage(BasePage):
    _FIRST_NAME      = (By.ID, "first-name")
    _LAST_NAME       = (By.ID, "last-name")
    _POSTAL_CODE     = (By.ID, "postal-code")
    _CONTINUE_BTN    = (By.ID, "continue")
    _ERROR_MSG       = (By.CSS_SELECTOR, "[data-test='error']")
    _FINISH_BTN      = (By.ID, "finish")
    _SUMMARY_ITEMS   = (By.CLASS_NAME, "cart_item")
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_personal_info(self, first_name, last_name, postal_code):
        self._type(self._FIRST_NAME, first_name)
        self._type(self._LAST_NAME, last_name)
        self._type(self._POSTAL_CODE, postal_code)
        return self

    def continue_to_step_two(self):
        self._click(self._CONTINUE_BTN)
        return self

    def get_error_message(self):
        return self._text(self._ERROR_MSG)

    def get_summary_items(self):
        return self.driver.find_elements(*self._SUMMARY_ITEMS)

    def finish_purchase(self):
        self._click(self._FINISH_BTN)
        return self

    def get_confirmation_header(self):
        return self._text(self._COMPLETE_HEADER)

    def is_order_confirmed(self):
        return self._is_visible(self._COMPLETE_HEADER)