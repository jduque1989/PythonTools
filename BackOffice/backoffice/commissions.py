
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import csv
import time


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def login(driver, url, username, password):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "myusername"))).send_keys(username)
    driver.find_element(By.ID, "mypassword").send_keys(password)
    driver.find_element(By.ID, "myloginbtn").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Label2")))


# def navigate_to_commissions(driver, url):
#     driver.get(url)
#     WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "demo03"))).click()


def select_country(driver, country_value="170"):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "commissioncountrydd")))
    Select(driver.find_element(By.ID, "commissioncountrydd")).select_by_value(country_value)


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


def print_table_data(driver):
    csv_file_path = 'commission.csv'
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        rows = driver.find_elements(By.XPATH, "//tbody[@id='datarow']/tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = [cell.text for cell in cells]
            writer.writerow(row_data)
            print(row_data)
    print(f"Data written to {csv_file_path}")


if __name__ == "__main__":
    driver = initialize_driver()
    load_dotenv('teamcv/.env')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    login(driver, "https://colombia.ganoexcel.com/Commissions.aspx", username, password)
    click_element(driver, By.ID, "demo03")
    select_country(driver, "170")
    time.sleep(1)
    print_table_data(driver)
    driver.quit()
