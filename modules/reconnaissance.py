import requests

class Reconnaissance:
    def __init__(self):
        pass

    def perform_reconnaissance(self, target_url):
        response = requests.get(target_url)
        print(f"Reconnaissance on {target_url}")
        if response.status_code == 200:
            print("Target is live!")
            print("Headers:", response.headers)
            print("Cookies:", response.cookies)
        else:
            print(f"Failed to reach {target_url}, Status Code: {response.status_code}")
