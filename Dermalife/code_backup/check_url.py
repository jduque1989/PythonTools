import requests
import time
from datetime import datetime

def log_status(message):
    with open("check_status_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

def check_website_status(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        response = requests.get(url, headers=headers)
        status_message = f"Website {url} returned status code: {response.status_code}"
        print(status_message)
        log_status(status_message)
    except requests.ConnectionError:
        error_message = f"Failed to connect to {url}. The website may be down."
        print(error_message)
        log_status(error_message)

if __name__ == "__main__":
    url = "https://dermalife.co/wp-admin"
    end_time = time.time() + 60*60  # Run for 1 hour
    while time.time() < end_time:
        check_website_status(url)
        time.sleep(120)  # Sleep for 2 minutes

