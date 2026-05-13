from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(service=Service(), options=options)
wait = WebDriverWait(driver, 10)

# Login
driver.get("https://www.saucedemo.com/")
wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
driver.find_element(By.ID, "password").send_keys("secret_sauce")
driver.find_element(By.ID, "login-button").click()
wait.until(EC.url_contains("inventory"))

# Adiciona produto
wait.until(EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
time.sleep(1)

# Vai ao carrinho
driver.get("https://www.saucedemo.com/cart.html")
time.sleep(2)
print(f"URL carrinho: {driver.current_url}")
print(f"Itens: {len(driver.find_elements(By.CLASS_NAME, 'cart_item'))}")

# Tenta navegar direto para checkout
driver.get("https://www.saucedemo.com/checkout-step-one.html")
time.sleep(2)
print(f"URL checkout direto: {driver.current_url}")

# Preenche formulario
wait.until(EC.presence_of_element_located((By.ID, "first-name"))).send_keys("Joao")
driver.find_element(By.ID, "last-name").send_keys("Silva")
driver.find_element(By.ID, "postal-code").send_keys("64000000")
time.sleep(1)

driver.find_element(By.ID, "continue").click()
time.sleep(2)
print(f"URL apos continue: {driver.current_url}")

driver.quit()