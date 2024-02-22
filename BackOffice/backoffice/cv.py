
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def login(driver, url, username, password):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "myusername"))).send_keys(username)
    driver.find_element(By.ID, "mypassword").send_keys(password)
    driver.find_element(By.ID, "myloginbtn").click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Label2")))


def navigate_to_downline(driver, url):
    driver.get(url)
    print(f"Navigated to {url}")


def click_binary_tree_button(driver):
    # Wait for the button to be clickable
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "demo01"))
    )
    # Click the button
    button.click()

def check_for_correct_page(driver):
    try:
        # Wait for the specific div element to be present on the page
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'div-child-node ng-binding') and contains(text(), 'GRUPO MERAKI SAS')]"))
        )
        # If the element is found, print confirmation message
        print("Successfully navigated to the correct page!")
        return True
    except:
        # If the element is not found, print an error message
        print("Failed to navigate to the correct page.")
        return False

def click_grupo_meraki_sas(driver):
    # Use an XPath expression that targets the div based on its class and contained text
    xpath_expression = "//div[contains(@class, 'div-child-node ng-binding') and contains(text(), 'GRUPO MERAKI SAS')]"
    try:
        # Wait for the element to be clickable
        grupo_meraki_sas_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath_expression))
        )
        # Click the element
        grupo_meraki_sas_element.click()
        print("Clicked on 'GRUPO MERAKI SAS'.")
    except TimeoutException:
        print("Failed to click on 'GRUPO MERAKI SAS' within the timeout period.")


def click_resumen_del_ciclo_actual(driver):
    try:
        # Use an XPath expression that targets the button based on its text
        button_xpath = "//button[contains(@class, 'GE_ItemBtn_FullWidth') and text()='Resumen del Ciclo Actual']"
        # Wait for the button to be clickable
        resumen_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )
        # Click the button
        resumen_button.click()
        print("Clicked on 'Resumen del Ciclo Actual' button.")
    except TimeoutException:
        print("Failed to click on 'Resumen del Ciclo Actual' button within the timeout period.")


def print_specific_table_contents(driver):
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


def separate():
    print("\n")
    print("****************************************************")


def print_division_data(driver):
    # Wait for the content to be loaded
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "w3-cell-row")))

    # Define the labels for data points
    left_labels = ["Total Vendedores Independientes", "Inscritos Personales Activos", 
                   "GCV Semana Actual", "GCV Semana Anterior"]
    right_labels = ["Total Afiliados", "Inscritos Activos", "GCV Semana Actual", 
                    "GCV Semana Anterior"]

    # Extract and print data for the left side
    print("RAMA IZQUIERDA:")
    left_data_elements = driver.find_elements(By.CSS_SELECTOR, ".PanellLeftSide h6 .ng-binding")
    for label, data_element in zip(left_labels, left_data_elements):
        print(f"{label}: {data_element.text}")

    print("\nRAMA DERECHA:")
    # Extract and print data for the right side
    right_data_elements = driver.find_elements(By.CSS_SELECTOR, ".PanellRightSide h6 .ng-binding")
    for label, data_element in zip(right_labels, right_data_elements):
        print(f"{label}: {data_element.text}")


def screenshot(driver):
    driver.set_window_size(720, 1568)
    screenshot_file_path = "./screenshot.png"
    time.sleep(1)
    driver.save_screenshot(screenshot_file_path)
    print(f"Screenshot saved to {screenshot_file_path}")


if __name__ == "__main__":
    driver = initialize_driver()
    login(driver, "https://colombia.ganoexcel.com/Home.aspx", "4844394", "112358")
    time.sleep(2)
    print_division_data(driver)
    navigate_to_downline(driver, "https://colombia.ganoexcel.com/Downline.aspx")
    click_binary_tree_button(driver)
    check_for_correct_page(driver)
    click_grupo_meraki_sas(driver)
    click_resumen_del_ciclo_actual(driver)
    separate()
    print_specific_table_contents(driver)
    separate()
    screenshot(driver)

    driver.quit()
