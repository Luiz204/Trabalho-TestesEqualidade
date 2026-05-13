from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from web_tests.pages.base_page import BasePage
import time

class CheckoutPage(BasePage):
    _FIRST_NAME      = (By.ID, "first-name")
    _LAST_NAME       = (By.ID, "last-name")
    _POSTAL_CODE     = (By.ID, "postal-code")
    _CONTINUE_BTN    = (By.CSS_SELECTOR, "input[data-test='continue']")
    _ERROR_MSG       = (By.CSS_SELECTOR, "[data-test='error']")
    _FINISH_BTN      = (By.CSS_SELECTOR, "button[data-test='finish']")
    _SUMMARY_ITEMS   = (By.CLASS_NAME, "cart_item")
    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def fill_personal_info(self, first_name, last_name, postal_code):
        self.wait.until(EC.presence_of_element_located(self._FIRST_NAME)).send_keys(first_name)
        self.driver.find_element(*self._LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self._POSTAL_CODE).send_keys(postal_code)
        time.sleep(1)
        return self

    def continue_to_step_two(self):
        btn = self.wait.until(EC.element_to_be_clickable(self._CONTINUE_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)
        return self

    def get_error_message(self):
        return self._text(self._ERROR_MSG)

    def get_summary_items(self):
        self.wait.until(EC.presence_of_all_elements_located(self._SUMMARY_ITEMS))
        return self.driver.find_elements(*self._SUMMARY_ITEMS)

    def finish_purchase(self):
        btn = self.wait.until(EC.element_to_be_clickable(self._FINISH_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(2)
        return self

    def get_confirmation_header(self):
        return self._text(self._COMPLETE_HEADER)

    def is_order_confirmed(self):
        return self._is_visible(self._COMPLETE_HEADER)