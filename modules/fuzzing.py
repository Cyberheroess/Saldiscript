import requests
import string
import random

def fuzz_url(url):
    chars = string.ascii_letters + string.digits + string.punctuation
    for char in chars:
        full_url = f"{url}?input={char}"
        try:
            response = requests.get(full_url)
            if response.status_code != 200:
                print(f"Fuzzing detected issue with char: {char}, Status: {response.status_code}")
            else:
                print(f"Input {char} is fine")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# Contoh penggunaan:
# fuzz_url("http://target.com/submit")
