import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from web_tests.pages.base_page import BasePage

class CartPage(BasePage):
    _CART_ITEMS   = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES   = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BTN = (By.ID, "checkout")
    _REMOVE_BTN   = (By.XPATH, "//button[contains(@id,'remove')]")
    _PAGE_TITLE   = (By.CLASS_NAME, "title")

    def _wait_for_page(self):
        self.wait.until(EC.url_contains("cart"))
        self.wait.until(EC.presence_of_element_located(self._PAGE_TITLE))
        time.sleep(1)

    def get_cart_items(self):
        self._wait_for_page()
        return self.driver.find_elements(*self._CART_ITEMS)

    def get_item_names(self):
        self._wait_for_page()
        return [el.text for el in self.driver.find_elements(*self._ITEM_NAMES)]

    def get_cart_count(self):
        return len(self.get_cart_items())

    def is_empty(self):
        return self.get_cart_count() == 0

    def proceed_to_checkout(self):
        self._wait_for_page()
        element = self.wait.until(EC.presence_of_element_located(self._CHECKOUT_BTN))
        self.driver.execute_script("arguments[0].click();", element)
        return self

    def remove_first_item(self):
        self._wait_for_page()
        buttons = self.driver.find_elements(*self._REMOVE_BTN)
        if buttons:
            self.driver.execute_script("arguments[0].click();", buttons[0])
        return self