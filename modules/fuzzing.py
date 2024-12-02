import random

class Fuzzing:
    def __init__(self):
        pass

    def fuzz_url(self, url):
        fuzz_payloads = ["' OR 1=1 --", "<script>alert('XSS')</script>", "DROP TABLE users;"]
        payload = random.choice(fuzz_payloads)
        fuzzed_url = f"{url}?input={payload}"
        print(f"Fuzzing URL: {fuzzed_url}")
        return fuzzed_url
