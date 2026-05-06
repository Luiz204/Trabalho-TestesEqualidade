import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from web_tests.pages.login_page import LoginPage

VALID_USER     = "standard_user"
VALID_PASSWORD = "secret_sauce"

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    browser = webdriver.Chrome(service=Service(), options=options)
    browser.implicitly_wait(5)
    yield browser
    browser.quit()

@pytest.fixture
def logged_in_driver(driver):
    LoginPage(driver).open().login(VALID_USER, VALID_PASSWORD)
    return driver