import requests
import csv
from datetime import datetime, timedelta
import os
import time
import subprocess

# Specify the path to your CSV file

csv_file_path = 'commission.csv'  # Replace with the actual path to your CSV file

max_wait_time = 60  # For example, wait for a maximum of 60 seconds
start_time = time.time()

# Check if the CSV file exists and is not empty
if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
    print(f"The file {csv_file_path} exists and is not empty.")
else:
    print(f"The file {csv_file_path} is empty or does not exist. Running the script.")
    subprocess.Popen(['python', 'commissions.py'])
    while not os.path.exists(csv_file_path):
        elapsed_time = int(time.time() - start_time)  # Calculate elapsed time in seconds
        if elapsed_time > max_wait_time:
            print(f"\nMaximum waiting time of {max_wait_time} seconds exceeded.")
            break  # Exit the loop if max waiting time is exceeded
        print(f"\rWaiting time: {elapsed_time} seconds", end="")
        time.sleep(1)
# Wait for 1 second before checking again

    print()
    if os.path.exists(csv_file_path):
        print(f"{csv_file_path} has been created.")
    else:
        print(f"{csv_file_path} was not created within the maximum wait time.")

# Initialize an empty list to store the first row
first_row = []

# Open the CSV file for reading
with open(csv_file_path, mode='r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    # Read the first row from the file and save it
    first_row = next(reader, None)  # Returns None if the file is empty

# At this point, 'first_row' contains the first row from the CSV file as a list
print(first_row)
url = "https://api.alegra.com/api/v1/invoices"


if first_row:
    price_tag = first_row[4]
    ciclo_tag = first_row[0]
    fecha_tag = first_row[1]
    monto_tag = first_row[5]
else:
    print("CSV file is empty or could not be read properly.")

today_date = datetime.now().strftime("%Y-%m-%d")
day_of_week = datetime.now().weekday()  # Monday is 0, Sunday is 6
days_until_next_friday = (4 - day_of_week) % 7  # Friday is 4
if days_until_next_friday == 0:
    days_until_next_friday = 7  # If today is Friday, set next Friday to 7 days ahead
next_friday = datetime.now() + timedelta(days=days_until_next_friday)
next_friday_formatted = next_friday.strftime("%Y-%m-%d")
# monto_cop = float(monto_tag.replace("$", "")) * 3990
monto_cop = float(monto_tag.replace("$", "").replace(",", "")) * 3990
print(monto_cop)
payload = {
    "numberTemplate": {"id": "23"},
    "client": {"id": 1},
    "anotation": "*FAVOR NO EFECTUAR RETENCION EN LA FUENTE* Regimen simple de tributación.  Medio de pago por transferencia electrónica a la CUENTA DE AHORROS 28070119350 de BANCOLOMBIA, a NOMBRE DE GRUPO MERAKI.  Autorizo en caso de incumplimiento de esta obligación sea reportado a las centrales",
    "items": [
        {
            "stamp": {"generateStamp": False},
            "id": 5,
            "name": "COMPENSACIÓN",
            "price": monto_cop,
            "description": f"CICLO {ciclo_tag} - Fechas de corte: {fecha_tag}. MONTO DOLARES: {monto_tag}",
            "quantity": 1,
            "tax": [{"id": 3}]
        }
    ],
    "date": today_date,
    "dueDate": next_friday_formatted,
    "paymentForm": "CREDIT",
    "status": "draft"
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": "Basic bWVyYWtpQGp1YW5kdXF1ZS5tZTo2MDExNWM0YTBlNDc3MDcxNjgwMA=="
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200 or response.status_code == 201:  # 200 OK or 201 Created are typically success statuses
    print("Invoice created successfully.")
else:
    print(f"Failed to create invoice. Status code: {response.status_code}, Message: {response.text}")
