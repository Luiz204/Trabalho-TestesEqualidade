from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from web_tests.pages.base_page import BasePage
import time

class InventoryPage(BasePage):
    _TITLE         = (By.CLASS_NAME, "title")
    _PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CART_BADGE    = (By.CLASS_NAME, "shopping_cart_badge")

    def is_on_inventory_page(self):
        return self._is_visible(self._TITLE)

    def get_page_title(self):
        return self._text(self._TITLE)

    def get_product_names(self):
        self.wait.until(EC.presence_of_all_elements_located(self._PRODUCT_NAMES))
        return [el.text for el in self.driver.find_elements(*self._PRODUCT_NAMES)]

    def get_cart_count(self):
        try:
            return int(self._text(self._CART_BADGE))
        except Exception:
            return 0

    def add_product_by_slug(self, slug):
        locator = (By.ID, f"add-to-cart-{slug}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()
        time.sleep(1)
        return self

    def go_to_cart(self):
        self.driver.get("https://www.saucedemo.com/cart.html")
        time.sleep(2)
        return self