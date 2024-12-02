import random
import string
import requests

class Fuzzing:
    def __init__(self, target_url):
        self.target_url = target_url

    def fuzz(self, param):
        payload = self._generate_random_payload()
        response = requests.get(self.target_url, params={param: payload})
        return response.text

    def _generate_random_payload(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))
