import requests
import logging

logger = logging.getLogger(__name__)

class Reconnaissance:
    def __init__(self, target_url):
        self.target_url = target_url

    def scan(self):
        """
        Melakukan pemindaian terhadap target untuk mengetahui potensi kerentanannya.
        """
        try:
            response = requests.get(self.target_url)
            if response.status_code == 200:
                logger.info(f"Target is online and reachable: {self.target_url}")
            else:
                logger.warning(f"Target is not reachable: {self.target_url}")
        except Exception as e:
            logger.error(f"Error during reconnaissance: {str(e)}")

# Contoh penggunaan:
# recon = Reconnaissance("http://example.com")
# recon.scan()
