
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
import logging
from datetime import datetime, timedelta
import time
import subprocess

# Configure logging
logging.basicConfig(filename='order_history.log', level=logging.INFO, 
                    format='%(asctime)s:%(levelname)s:%(message)s')


def initialize_driver():
    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def login(driver, url, username, password):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "myusername"))).send_keys(username)
    driver.find_element(By.ID, "mypassword").send_keys(password)
    driver.find_element(By.ID, "myloginbtn").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Label2")))


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


def calculate_cycle(order_date):
    reference_date = datetime.strptime("2024-01-01", "%Y-%m-%d")  # Example reference date
    reference_cycle = 787  # Example reference cycle number

    order_date_dt = datetime.strptime(order_date, "%m/%d/%Y")
    days_diff = (order_date_dt - reference_date).days
    cycle_number = reference_cycle + (days_diff // 7)

    return cycle_number


def log_orders(orders):
    for order in orders:
        logging.info(f"Order: {order['orden']}, Fecha de Orden: {order['fecha_de_orden']}, "
                     f"Total de Orden: {order['total_de_orden']}, Total PV: {order['total_pv']}, Cicle: {order['cicle']}")


def print_orders(orders):
    print(f"Printing {len(orders)} orders")  # Debug print
    for order in orders:
        print(f"Order: {order['orden']}, Fecha de Orden: {order['fecha_de_orden']}, "
              f"Total de Orden: {order['total_de_orden']}, Total PV: {order['total_pv']}, Cicle: {order['cicle']}")


def get_current_cycle():
    reference_date = datetime.strptime("2024-01-01", "%Y-%m-%d")  # Example reference date
    reference_cycle = 787  # Example reference cycle number

    current_date = datetime.now()
    days_diff = (current_date - reference_date).days
    cycle_number = reference_cycle + (days_diff // 7)

    return cycle_number


def predict_next_purchase_cycle(relevant_orders, current_cycle, total_pv):
    if not relevant_orders:
        return None, 50  # Assumes next purchase cycle is 4 cycles from now and requires 50 PV

    latest_purchase_cycle = max(order['cicle'] for order in relevant_orders)
    if total_pv < 50:
        next_purchase_cycle = current_cycle
        pv_required = 50 - total_pv
    else:
        next_purchase_cycle = latest_purchase_cycle + 4
        pv_in_next_purchase_cycle = sum(order['total_pv'] for order in relevant_orders if order['cicle'] == next_purchase_cycle)
        pv_required = max(0, 50 - pv_in_next_purchase_cycle)    


    return next_purchase_cycle, pv_required


def check_pv_warning(current_cycle, pv_orders):
    relevant_orders = [order for order in pv_orders if current_cycle >= order['cicle'] >= current_cycle - 3]
    pv_current_cycle = sum(order['total_pv'] for order in relevant_orders)
    relevant_orders = [order for order in pv_orders if current_cycle >= order['cicle'] >= current_cycle - 2]
    pv_next_cycle = sum(order['total_pv'] for order in relevant_orders)

    if pv_current_cycle < 50:
        print(f"Peligro: PV en el ciclo actual ({current_cycle}) es menor de 50. PV actuales : {pv_current_cycle}")
    if pv_next_cycle < 50:
        print(f"Peligro: PV en el ciclo actual ({current_cycle + 1}) se proyecta estar por debajo de 50. Proyección PV: {pv_next_cycle}")


def navigate_to(driver, url):
    driver.get(url)
    print(f"Navigated to {url}")


def wait_for_element(driver, by, identifier):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, identifier)))


def take_screenshot(driver, code, file_path=".png"):
    driver.set_window_size(1280, 1568)
    time.sleep(1)  # Consider using WebDriverWait here instead of time.sleep
    file_path = code + file_path
    driver.save_screenshot(file_path)
    print(f"Screenshot saved to {file_path}")
    subprocess.run(["open", file_path])


def get_order_history(driver):
    try:
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "myOrderHistory"))
        )
    except Exception as e:
        logging.error(f"Order history table not found: {e}")
        print(f"Order history table not found: {e}")  # Debug print
        return []

    orders = []
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        if len(columns) < 4:
            continue
        order_date = columns[1].text.strip()
        try:
            total_pv = float(columns[3].text.strip().replace(',', ''))
        except ValueError:
            total_pv = 0.0
        order = {
            'orden': columns[0].text.strip(),
            'fecha_de_orden': order_date,
            'total_de_orden': columns[2].text.strip(),
            'total_pv': total_pv,
            'cicle': calculate_cycle(order_date)
        }
        orders.append(order)
        logging.info(f"Order captured: {order}")

    return orders


def main():
    current_cycle = get_current_cycle()
    print(f"El ciclo actual es: {current_cycle}")
    
    with initialize_driver() as driver:
        load_dotenv('.env')
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        login(driver, "https://colombia.ganoexcel.com/Login.aspx", username, password)
        navigate_to(driver, "https://colombia.ganoexcel.com/Ordering.aspx")
        click_element(driver, By.ID, "demo02")
        wait_for_element(driver, By.ID, "myOrderHistory")
        time.sleep(3)
        orders = get_order_history(driver)
        for order in orders:
            print(order)
        orders = get_order_history(driver)
        print(f"Número de ordenes que estamos revisando: {len(orders)}")  # Debug print
        if orders:
            pv_orders = [order for order in orders if order['total_pv'] > 0]
            relevant_orders = [order for order in pv_orders if current_cycle >= order['cicle'] >= current_cycle - 3]
            print(f"Las ordenes de los ultimos 4 ciclos incluyendo el actual son: {len(relevant_orders)}")
            print_orders(relevant_orders)
        #     log_orders(relevant_orders)
            total_pv = sum(order['total_pv'] for order in relevant_orders)
            print("\n")
            print("Resumen")
            print(f"Total PV de las ordenes relevantes: {total_pv}")

            next_purchase_cycle, pv_required = predict_next_purchase_cycle(relevant_orders, current_cycle, total_pv)
            if next_purchase_cycle:
                print(f"La siguiente compra se debe hacer en el ciclo: {next_purchase_cycle}, debes comprar al menos {pv_required} PV para estar por encima de 50 PV.")
            else:
                print("No se encontraron ordenes relevantes. Debes comprar al menos 50PV en este ciclo.")

            check_pv_warning(current_cycle, pv_orders)
        else:
            logging.info("No orders found.")
            print("No orders found.")  # Debug print
        take_screenshot(driver, username)
        driver.quit()


if __name__ == "__main__":
    main()
