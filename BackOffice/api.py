import requests

url = "https://api.alegra.com/api/v1/invoices/id"

headers = {
    "accept": "application/json",
    "authorization": "Basic bWVyYWtpQGp1YW5kdXF1ZS5tZTo0YTEwNjJiNzkzMjFmYmQ2MjI1YQ=="}

response = requests.get(url, headers=headers)

print(response.text)
