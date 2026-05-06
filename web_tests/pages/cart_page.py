from selenium.webdriver.common.by import By
from web_tests.pages.base_page import BasePage

class CartPage(BasePage):
    _CART_ITEMS   = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES   = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BTN = (By.ID, "checkout")
    _REMOVE_BTN   = (By.XPATH, "//button[contains(@id,'remove')]")

    def get_cart_items(self):
        return self.driver.find_elements(*self._CART_ITEMS)

    def get_item_names(self):
        return [el.text for el in self.driver.find_elements(*self._ITEM_NAMES)]

    def get_cart_count(self):
        return len(self.get_cart_items())

    def is_empty(self):
        return self.get_cart_count() == 0

    def proceed_to_checkout(self):
        self._click(self._CHECKOUT_BTN)
        return self

    def remove_first_item(self):
        buttons = self.driver.find_elements(*self._REMOVE_BTN)
        if buttons:
            buttons[0].click()
        return self
    