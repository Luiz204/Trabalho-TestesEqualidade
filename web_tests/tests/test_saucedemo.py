import pytest
from web_tests.pages.login_page import LoginPage
from web_tests.pages.inventory_page import InventoryPage
from web_tests.pages.cart_page import CartPage
from web_tests.pages.checkout_page import CheckoutPage

VALID_USER     = "standard_user"
VALID_PASSWORD = "secret_sauce"

class TestLoginFlow:
    def test_login_with_valid_credentials(self, driver):
        LoginPage(driver).open().login(VALID_USER, VALID_PASSWORD)
        assert "inventory" in driver.current_url

    def test_login_with_invalid_password(self, driver):
        login = LoginPage(driver).open()
        login.login(VALID_USER, "senha_errada")
        assert login.is_error_visible()
        assert "Epic sadface" in login.get_error_message()

    def test_login_with_locked_user(self, driver):
        login = LoginPage(driver).open()
        login.login("locked_out_user", VALID_PASSWORD)
        assert login.is_error_visible()
        assert "locked out" in login.get_error_message().lower()

    def test_login_with_empty_credentials(self, driver):
        login = LoginPage(driver).open()
        login.login("", "")
        assert login.is_error_visible()

class TestInventoryPage:
    def test_inventory_page_loads_after_login(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        assert inventory.is_on_inventory_page()
        assert inventory.get_page_title() == "Products"

    def test_products_are_listed(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        assert len(inventory.get_product_names()) > 0

    def test_add_product_to_cart_updates_badge(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        assert inventory.get_cart_count() == 0
        inventory.add_product_by_slug("sauce-labs-backpack")
        assert inventory.get_cart_count() == 1

    def test_add_multiple_products_updates_badge(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product_by_slug("sauce-labs-backpack")
        inventory.add_product_by_slug("sauce-labs-bike-light")
        assert inventory.get_cart_count() == 2

class TestCartFlow:
    def test_cart_shows_added_product(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product_by_slug("sauce-labs-backpack")
        inventory.go_to_cart()
        cart = CartPage(logged_in_driver)
        assert cart.get_cart_count() == 1
        assert "Sauce Labs Backpack" in cart.get_item_names()

    def test_cart_shows_multiple_products(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product_by_slug("sauce-labs-backpack")
        inventory.add_product_by_slug("sauce-labs-bike-light")
        inventory.go_to_cart()
        assert CartPage(logged_in_driver).get_cart_count() == 2

    def test_remove_item_from_cart(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product_by_slug("sauce-labs-backpack")
        inventory.go_to_cart()
        cart = CartPage(logged_in_driver)
        cart.remove_first_item()
        assert cart.is_empty()

class TestCheckoutE2E:
    def test_complete_purchase_flow(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product_by_slug("sauce-labs-backpack")
        inventory.go_to_cart()
        CartPage(logged_in_driver).proceed_to_checkout()
        checkout = CheckoutPage(logged_in_driver)
        checkout.fill_personal_info("Joao", "Silva", "64000-000")
        checkout.continue_to_step_two()
        assert len(checkout.get_summary_items()) == 1
        checkout.finish_purchase()
        assert checkout.is_order_confirmed()
        assert "Thank you" in checkout.get_confirmation_header()

    def test_checkout_requires_personal_info(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product_by_slug("sauce-labs-backpack")
        inventory.go_to_cart()
        CartPage(logged_in_driver).proceed_to_checkout()
        checkout = CheckoutPage(logged_in_driver)
        checkout.continue_to_step_two()
        assert "Error" in checkout.get_error_message()

    def test_complete_purchase_with_two_products(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product_by_slug("sauce-labs-backpack")
        inventory.add_product_by_slug("sauce-labs-fleece-jacket")
        inventory.go_to_cart()
        CartPage(logged_in_driver).proceed_to_checkout()
        checkout = CheckoutPage(logged_in_driver)
        checkout.fill_personal_info("Maria", "Souza", "01310-100")
        checkout.continue_to_step_two()
        assert len(checkout.get_summary_items()) == 2
        checkout.finish_purchase()
        assert checkout.is_order_confirmed()