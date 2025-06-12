from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Danh sách tài khoản cần thử
accounts = [
    {"username": "standard_user", "password": "secret_sauce"},
    {"username": "locked_out_user", "password": "secret_sauce"},
    {"username": "problem_user", "password": "secret_sauce"},
    {"username": "performance_glitch_user", "password": "secret_sauce"},
    {"username": "error_user", "password": "secret_sauce"},
    {"username": "visual_user", "password": "secret_sauce"}
]

# Khởi tạo trình duyệt
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)
all_products = []

for account in accounts:
    driver.get("https://www.saucedemo.com/")

    try:
        wait.until(EC.presence_of_element_located((By.ID, "user-name")))

        driver.find_element(By.ID, "user-name").clear()
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "user-name").send_keys(account["username"])
        driver.find_element(By.ID, "password").send_keys(account["password"])
        driver.find_element(By.ID, "login-button").click()

        if driver.find_elements(By.CLASS_NAME, "error-message-container"):
            print(f"Login failed for user: {account['username']}")
            continue

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_item")))

        names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")

        for name, price in zip(names, prices):
            all_products.append({
                "Username": account["username"],
                "Product Name": name.text,
                "Price": price.text
            })

        print(f"Collected data for user: {account['username']}") 

    except Exception as e:
        print(f"Error for user {account['username']}: {e}")

    df = pd.DataFrame(all_products)
    df.to_excel("saucedemo_products.xlsx", index=False)

driver.quit()
