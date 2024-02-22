import requests
import random
import csv
import os
import threading

words_cache = []
csv_file_path = 'words_cache.csv'


def fetch_words_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return [word for word in response.text.split() if len(word) >= 4]
    return []


def update_csv_file(url):
    new_words = fetch_words_from_url(url)
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for word in new_words:
            writer.writerow([word])


def fetch_words(url='https://www.mit.edu/~ecprice/wordlist.100000'):
    if not os.path.exists(csv_file_path) or os.path.getsize(csv_file_path) == 0:
        update_csv_file(url)


def load_words_from_csv():
    global words_cache
    if not words_cache:
        if os.path.exists(csv_file_path) and os.path.getsize(csv_file_path) > 0:
            with open(csv_file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                words_cache = [row[0] for row in reader]


def get_word():
    if not words_cache:
        load_words_from_csv()
    return random.choice(words_cache) if words_cache else None


def update_csv_in_background(url):
    update_thread = threading.Thread(target=update_csv_file, args=(url,))
    update_thread.start()
    print("CSV file updated in the background.")


# Ensure CSV file is created if not present
fetch_words('https://www.mit.edu/~ecprice/wordlist.100000')
load_words_from_csv()
update_csv_in_background('https://www.mit.edu/~ecprice/wordlist.100000')
