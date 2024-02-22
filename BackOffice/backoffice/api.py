import requests
import base64

username = "meraki@juanduque.me"
password = "0b20bf7b5641170a3cc5"
combined = f"{username}:{password}"
encoded = base64.b64encode(combined.encode()).decode()
print(encoded)
url = "https://api.alegra.com/api/v1/invoices/559"

headers = {
    "accept": "application/json",
    "authorization": "Basic " + encoded
}

response = requests.get(url, headers=headers)

print(response.text)
