import random
import string
import requests

class Fuzzer:
    def __init__(self, target_url):
        self.target_url = target_url

    def generate_fuzzing_payload(self):
        """
        Generate a random payload to test for vulnerabilities like XSS, SQL injection, etc.
        """
        characters = string.ascii_letters + string.digits + string.punctuation
        length = random.randint(5, 15)
        payload = ''.join(random.choice(characters) for i in range(length))

        # Introduce common attack patterns
        if random.choice([True, False]):
            payload += "' OR 'a'='a"  # SQL Injection pattern
        else:
            payload += "<script>alert('XSS')</script>"  # XSS pattern

        return payload

    def test_payload(self, payload):
        """
        Send the fuzzing payload to the target and analyze the response.
        """
        try:
            response = requests.get(self.target_url, params={'input': payload})
            if "error" in response.text:
                print(f"Potential vulnerability detected with payload: {payload}")
            else:
                print(f"Payload {payload} executed successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error testing payload {payload}: {e}")

    def run_fuzzing(self, iterations=100):
        """
        Run fuzzing with random payloads for a given number of iterations.
        """
        for _ in range(iterations):
            payload = self.generate_fuzzing_payload()
            self.test_payload(payload)
