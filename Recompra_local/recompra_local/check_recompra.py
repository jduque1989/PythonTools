from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import subprocess
import time
from bs4 import BeautifulSoup
from datetime import datetime
import pytz


def initialize_driver():
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
    # return webdriver.Chrome(service=service, options=options)


def login(driver, url, username, password):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "myusername"))).send_keys(username)
    driver.find_element(By.ID, "mypassword").send_keys(password)
    driver.find_element(By.ID, "myloginbtn").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Label2")))


def navigate_to(driver, url):
    driver.get(url)
    print(f"Navigated to {url}")


def click_element(driver, by, identifier):
    # Wait for the element to be present on the page
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, identifier)))
    # Attempt to click the element using Selenium's click method
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, identifier)))
        element.click()
    except TimeoutException:
        # If the element is not clickable, fall back to JavaScript click
        element = driver.find_element(by, identifier)
        driver.execute_script("arguments[0].click();", element)


def wait_for_element(driver, by, identifier):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, identifier)))


def print_specific_table_data(driver):
    # Ensure the table is present
    custom_headers = [
        "Ciclo",
        "Periodo",
        "PV del Ciclo",
        "Rango Estimado",
        "Inscritos Total"
    ]


def take_screenshot(driver, code, file_path=".png"):
    driver.set_window_size(1280, 1568)
    time.sleep(1)  # Consider using WebDriverWait here instead of time.sleep
    file_path = code + file_path
    driver.save_screenshot(file_path)
    print(f"Screenshot saved to {file_path}")
    subprocess.run(["open", file_path])


def get_order_data(driver):

    orders_data = []

    # Locate the table rows containing order data
    order_rows = driver.find_elements(By.CSS_SELECTOR, '#myOrderHistory tbody .GE_tblRow')

    for row in order_rows:
        order = {}
        columns = row.find_elements(By.TAG_NAME, 'td')
        order['order_number'] = columns[0].text.strip()
        order['date_order'] = columns[1].text.strip()
        order['price_order'] = columns[2].text.strip()
        order['total_pv'] = columns[3].text.strip()
        orders_data.append(order)

    return orders_data


def get_current_cycle():
    reference_date = datetime.strptime("2024-01-01", "%Y-%m-%d")  # Example reference date
    reference_cycle = 787  # Example reference cycle number
    current_date = datetime.now()
    days_diff = (current_date - reference_date).days
    cycle_number = reference_cycle + (days_diff // 7)
    return cycle_number


def print_console(orders_data):
    for order in orders_data:
        print(order)


def main():
    with initialize_driver() as driver:
        load_dotenv('.env')
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        login(driver, "https://colombia.ganoexcel.com/Home.aspx", username, password)
        navigate_to(driver, "https://colombia.ganoexcel.com/Ordering.aspx")
        click_element(driver, By.ID, "demo02")
        wait_for_element(driver, By.ID, "myOrderHistory")
        print("Current cycle: ", get_current_cycle())
        orders = get_order_data(driver)
        print_console(orders)
        # print("Las ordenes de los ultimos 4 ciclos incluyendo el actual son:")
        # pv_orders = [order for order in orders if float(order['total_pv']) > 0]
        # current_cycle = get_current_cycle()
        # relevant_orders = [order for order in pv_orders if current_cycle >= order['cicle'] >= current_cycle - 3]
        # print_console(relevant_orders)
        # take_screenshot(driver, username)
        driver.quit()


if __name__ == "__main__":
    main()
