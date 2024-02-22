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
import pandas as pd


def initialize_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--incognito")
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


# def print_specific_table_data(driver):
#     # Ensure the table is present
#     custom_headers = [
#         "Ciclo",
#         "Periodo",
#         "PV del Ciclo",
#         "Rango Estimado",
#         "Inscritos Total"
#     ]

#     # Wait for the table to be present to ensure it's fully loaded
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.w3-hoverable")))

#     # Find all the rows in the specific table body
#     rows = driver.find_elements(By.XPATH, "//table[@class='w3-hoverable w3-table-all responsive']/tbody/tr")
#     count = 0
#     for row in rows:
#         # Extract the data cell text
#         data = row.find_element(By.TAG_NAME, "td").text
#         # Check if the data cell is not empty before printing
#         if data.strip() and count < len(custom_headers):
#             # .strip() removes any leading/trailing whitespace
#             header = custom_headers[count]  # Extract the header text
#             print(f"{header}: {data}")
#             count += 1
#         else:
#             # Optionally, you can print a message indicating an empty row, or simply pass
#             pass  # or print("Empty data for:", header)


def take_screenshot(driver, name, file_path_end=".png"):
    driver.set_window_size(720, 1568)
    time.sleep(1)  # Consider using WebDriverWait here instead of time.sleep
    file_path = name + file_path_end
    print(file_path)
    driver.save_screenshot(file_path)
    print(f"Screenshot saved to {file_path}")
    subprocess.run(["open", file_path])


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
    print(f"{'Left Branch Sum:':<20}{left_sum:>10} | {'Right Branch Sum:':<20}{right_sum:>10}")


def team_cvs(driver, code):
    # Wait for the input field to be clickable
    input_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[ng-model="SearchNode"]'))
    )
    # Find the input field by its ng-model attribute
    input_field = driver.find_element(By.CSS_SELECTOR, 'input[ng-model="SearchNode"]')
    # input_field = driver.find_element_by_css_selector('input[ng-model="SearchNode"]')

    # Type the number into the input field
    input_field.send_keys(code)  # replace '12345' with the number you want to input
    # Find the search button by its class (fa-search) and click it
    search_button = driver.find_element(By.CSS_SELECTOR, '.fa-search')
    search_button.click()


def read_csv_and_extract_columns():
    file_path = 'team_code.csv'  # Adjust the path as necessary
    delimiter = ';'
    id_column_name = 'ID'  # Adjust if the actual name is different
    name_column_name = 'NOMBRE '
    data = pd.read_csv(file_path, delimiter=delimiter)
    # Extract the specified columns
    IDs = data[id_column_name]
    Names = data[name_column_name]
    return IDs, Names


def loop_cv(driver):
    IDs, Names = read_csv_and_extract_columns()
    for i in range(0, len(IDs)):
        ids1 = str(IDs[i])
        name = str(Names[i])
        print(ids1)
        team_cvs(driver, ids1)
        print(Names[i])
        click_element(driver, By.XPATH, "//button[contains(@class, 'confirm')]")
        click_element(driver, By.XPATH, f"//div[contains(@class, 'ng-binding') and contains(text(), '{ids1}')]")
        click_element(driver, By.XPATH, "//button[contains(@class, 'GE_ItemBtn_FullWidth') and contains(text(), 'Resumen del Ciclo Actual')]")
        fetch_and_calculate_total_sum(driver)
        print(name)
        take_screenshot(driver, name)
        navigate_to(driver, "https://colombia.ganoexcel.com/Downline.aspx")
        click_element(driver, By.ID, "demo01")
        click_element(driver, By.ID, "optionpanelbtn")


def main():
    with initialize_driver() as driver:
        load_dotenv('.env')
        username = os.getenv('USERNAME')
        password = os.getenv('PASSWORD')
        login(driver, "https://colombia.ganoexcel.com/Home.aspx", username, password)
        # # Follow through the workflow, replacing specific calls with the more generic ones.
        navigate_to(driver, "https://colombia.ganoexcel.com/Downline.aspx")
        click_element(driver, By.ID, "demo01")
        click_element(driver, By.ID, "optionpanelbtn")
        loop_cv(driver)
        # IDs, Names = read_csv_and_extract_columns()
        # print(len(IDs))
        # ids1 = str(IDs[1])
        # print(IDs[0], Names[0])
        # team_cvs(driver, ids1)
        # click_element(driver, By.XPATH, "//button[contains(@class, 'confirm')]")
        # click_element(driver, By.XPATH, f"//div[contains(@class, 'ng-binding') and contains(text(), '{ids1}')]")
        # click_element(driver, By.XPATH, "//button[contains(@class, 'GE_ItemBtn_FullWidth') and contains(text(), 'Resumen del Ciclo Actual')]")
        # take_screenshot(driver, ids1)
        # # print_specific_table_data(driver)
        # fetch_and_calculate_total_sum(driver)


if __name__ == "__main__":
    main()
