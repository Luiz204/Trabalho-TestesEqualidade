import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from web_tests.pages.login_page import LoginPage
import time

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
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False
    })
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    chrome_binary = os.environ.get("CHROME_BINARY")
    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")

    if chrome_binary:
        options.binary_location = chrome_binary

    if chromedriver_path:
        service = Service(executable_path=chromedriver_path)
    else:
        service = Service()

    browser = webdriver.Chrome(service=service, options=options)
    browser.set_page_load_timeout(30)
    yield browser
    browser.quit()

@pytest.fixture
def logged_in_driver(driver):
    LoginPage(driver).open().login(VALID_USER, VALID_PASSWORD)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains("inventory"))
    time.sleep(1)
    return driver