import requests
from urllib.parse import urlparse

class Reconnaissance:
    def __init__(self):
        self.sensitive_headers = ['X-Powered-By', 'Server', 'X-Frame-Options', 'Strict-Transport-Security']

    def perform_reconnaissance(self, target_url):
        response = requests.get(target_url)
        print(f"Reconnaissance on {target_url}")
        
        if response.status_code == 200:
            print(f"{G}Target is live!{N}")
            self.print_headers(response.headers)
            self.print_cookies(response.cookies)
            self.detect_sensitive_info(response.text)
        else:
            print(f"{R}Failed to reach target. Status Code: {response.status_code}{N}")

    def print_headers(self, headers):
        print(f"Response Headers:")
        for header, value in headers.items():
            if header in self.sensitive_headers:
                print(f"{Y}{header}: {value}{N}")
            else:
                print(f"{C}{header}: {value}{N}")

    def print_cookies(self, cookies):
        print(f"Cookies: {cookies}")

    def detect_sensitive_info(self, content):
        # Search for sensitive information in the page content
        if "password" in content or "admin" in content:
            print(f"{Y}Potential sensitive information found in content!{N}")
        else:
            print(f"{C}No sensitive information detected in content.{N}")
