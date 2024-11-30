import random
import string
import logging

logger = logging.getLogger(__name__)

class AdaptivePayload:
    def __init__(self):
        self.payloads = []

    def generate_random_payload(self, length=10):
        """
        Membuat payload acak untuk menghindari deteksi.
        """
        payload = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        self.payloads.append(payload)
        return payload

    def test_payload(self, target_url, payload):
        """
        Mengirimkan payload untuk pengujian.
        """
        try:
            response = requests.get(target_url, params={"payload": payload})
            if "vulnerable" in response.text.lower():
                logger.info(f"Vulnerability found with payload: {payload}")
            else:
                logger.info(f"No vulnerability detected with payload: {payload}")
        except Exception as e:
            logger.error(f"Error during payload testing: {str(e)}")

    def execute(self, target_url):
        """
        Menjalankan payload adaptif untuk menghindari WAF atau IDS.
        """
        for payload in self.payloads:
            self.test_payload(target_url, payload)

# Contoh penggunaan:
# adaptive = AdaptivePayload()
# payload = adaptive.generate_random_payload()
# adaptive.execute("http://example.com/search")
