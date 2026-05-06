import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
    _PAGE_TITLE      = (By.CLASS_NAME, "title")
    _OVERVIEW_URL    = "checkout-step-two"

    def _wait_for_page(self):
        self.wait.until(EC.presence_of_element_located(self._PAGE_TITLE))
        time.sleep(1)

    def fill_personal_info(self, first_name, last_name, postal_code):
        self._wait_for_page()
        self._type(self._FIRST_NAME, first_name)
        self._type(self._LAST_NAME, last_name)
        self._type(self._POSTAL_CODE, postal_code)
        return self

    def continue_to_step_two(self):
        element = self.wait.until(EC.presence_of_element_located(self._CONTINUE_BTN))
        self.driver.execute_script("arguments[0].click();", element)
        try:
            self.wait.until(EC.url_contains(self._OVERVIEW_URL))
        except Exception:
            time.sleep(3)
        return self

    def get_error_message(self):
        try:
            return self._text(self._ERROR_MSG)
        except Exception:
            return ""

    def get_summary_items(self):
        try:
            self.wait.until(EC.presence_of_all_elements_located(self._SUMMARY_ITEMS))
        except Exception:
            time.sleep(2)
        return self.driver.find_elements(*self._SUMMARY_ITEMS)

    def finish_purchase(self):
        element = self.wait.until(EC.presence_of_element_located(self._FINISH_BTN))
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def get_confirmation_header(self):
        return self._text(self._COMPLETE_HEADER)

    def is_order_confirmed(self):
        return self._is_visible(self._COMPLETE_HEADER)