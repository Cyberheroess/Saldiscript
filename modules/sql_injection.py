import requests

class SQLInjection:
    def __init__(self, target_url):
        self.target_url = target_url

    def attack(self, payload):
        url = self.target_url + payload
        try:
            response = requests.get(url)
            if "error" in response.text or "warning" in response.text:
                print(f"Potential SQL Injection vulnerability found at: {url}")
            else:
                print(f"No vulnerability found for payload: {payload}")
        except requests.RequestException as e:
            print(f"Error during attack: {e}")
