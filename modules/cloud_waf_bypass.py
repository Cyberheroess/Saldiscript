import requests
import random

class CloudWAFBypass:
    def __init__(self, target_url):
        self.target_url = target_url

    def bypass_waf(self):
        headers = {
            "User-Agent": random.choice(["Mozilla/5.0", "Chrome/88.0", "Safari/537.36"]),
            "X-Forwarded-For": str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255))
        }
        try:
            response = requests.get(self.target_url, headers=headers)
            if response.status_code == 200:
                print(f"Bypassed WAF with headers: {headers}")
            else:
                print(f"WAF still blocking with status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error bypassing WAF: {e}")
