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
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)


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

    # Wait for the table to be present to ensure it's fully loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.w3-hoverable")))

    # Find all the rows in the specific table body
    rows = driver.find_elements(By.XPATH, "//table[@class='w3-hoverable w3-table-all responsive']/tbody/tr")
    count = 0
    for row in rows:
        # Extract the data cell text
        data = row.find_element(By.TAG_NAME, "td").text
        # Check if the data cell is not empty before printing
        if data.strip() and count < len(custom_headers):
            # .strip() removes any leading/trailing whitespace
            header = custom_headers[count]  # Extract the header text
            print(f"{header}: {data}")
            count += 1
        else:
            # Optionally, you can print a message indicating an empty row, or simply pass
            pass  # or print("Empty data for:", header)


def take_screenshot(driver, code, file_path=".png"):
    driver.set_window_size(720, 1568)
    time.sleep(1) # Consider using WebDriverWait here instead of time.sleep
    file_path = code + file_path
    driver.save_screenshot(file_path)
    print(f"Screenshot saved to {file_path}")
    subprocess.run(["open", file_path])


def print_right_side_data(driver):
    # Wait for the right panel to be present on the page
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".PanellRightSide"))
    )

    # Find the right side panel by its class
    right_panel = driver.find_element(By.CSS_SELECTOR, ".PanellRightSide")
    # Find all the 'span' elements with class 'ng-binding' within this panel
    right_side_values = right_panel.find_elements(By.CSS_SELECTOR, "h6 > span.ng-binding")
    count = 0
    # Print the text value of each 'span' element
    for value in right_side_values:
        count += 1
        if count == 3:
            cvs = value.text.strip()
            return cvs


def fetch_and_calculate_total_sum(driver):
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.select("table.w3-table.w3-striped.w3-border")
    country_data = {'left': [], 'right': []}
    # Process each table
    for index, table in enumerate(tables):
        branch = 'left' if index % 2 == 0 else 'right'
        rows = table.find_all('tr')
        start_summing = False
        for row in rows:
            cells = row.find_all('th')
            if cells and 'Vol. por País' in cells[0].text:
                start_summing = True
                continue
            if start_summing:
                country_cell = row.find('th')
                value_cell = row.find('td', class_='ng-binding')
                if country_cell and value_cell:
                    country = country_cell.text.strip()
                    value = value_cell.text.replace(',', '').strip()
                    if value.isdigit():
                        country_data[branch].append((country, int(value)))

    # Find the longer list to ensure we iterate through all entries
    max_length = max(len(country_data['left']), len(country_data['right']))
    # Print header
    print(f"{'Left Branch Country':<20}{'Value':>10} | {'Right Branch Country':<20}{'Value':>10}")
    print("-" * 70)
    # Print countries and values side by side
    for i in range(max_length):
        left_country = country_data['left'][i] if i < len(country_data['left']) else ("", "")
        right_country = country_data['right'][i] if i < len(country_data['right']) else ("", "")
        print(f"{left_country[0]:<20}{left_country[1]:>10} | {right_country[0]:<20}{right_country[1]:>10}")
    # Calculate and print total sums
    left_sum = sum(value for _, value in country_data['left'])
    right_sum = sum(value for _, value in country_data['right'])
    print("\nTotal Sums:")
    print(f"{'Left Branch Sum:':<20}{left_sum:>10} | {'Right Branch Sum:':<20}{right_sum:>10}")


def get_time(driver):
    wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
    update_time_element = wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(@class, 'ng-binding') and contains(., 'Hora del Pacífico')]")))
    update_time = update_time_element.text
    date_time_str = update_time[1:].split(' (')[0]
    format = '%m/%d/%Y %H:%M:%S'
    date_time_obj = datetime.strptime(date_time_str, format)
    print(date_time_obj, 'Hora Pacifico')
    pst_zone = pytz.timezone('America/Los_Angeles')
    cot_zone = pytz.timezone('America/Bogota')
    localized_pst_time = pst_zone.localize(date_time_obj)
    colombia_time = localized_pst_time.astimezone(cot_zone)
    print(colombia_time, 'Hora Colombia')


def main():
    with initialize_driver() as driver:
        load_dotenv('teamcv/.env')
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        login(driver, "https://colombia.ganoexcel.com/Home.aspx", username, password)
        cvs = print_right_side_data(driver)
        # Follow through the workflow, replacing specific calls with the more generic ones.
        navigate_to(driver, "https://colombia.ganoexcel.com/Downline.aspx")
        click_element(driver, By.ID, "demo01")
        click_element(driver, By.XPATH, f"//div[contains(@class, 'ng-binding') and contains(text(), '{username}')]")
        get_time(driver)
        click_element(driver, By.XPATH, "//button[contains(@class, 'GE_ItemBtn_FullWidth') and contains(text(), 'Resumen del Ciclo Actual')]")
        print_specific_table_data(driver)
        print("CVS: ", cvs)
        print("-" * 70)
        fetch_and_calculate_total_sum(driver)
        take_screenshot(driver, username)


if __name__ == "__main__":
    main()
