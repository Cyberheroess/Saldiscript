import requests

class Reconnaissance:
    def __init__(self, target_url):
        self.target_url = target_url

    def scan_target(self):
        response = requests.get(self.target_url)
        server_header = response.headers.get("Server")
        return server_header

    def get_technology(self):
        response = requests.get(self.target_url)
        if "WordPress" in response.text:
            return "WordPress"
        return "Unknown"
