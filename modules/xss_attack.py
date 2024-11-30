import requests

class XSSAttack:
    def __init__(self, target_url):
        self.target_url = target_url

    def attack(self, payload):
        data = {'search': payload}
        try:
            response = requests.post(self.target_url, data=data)
            if payload in response.text:
                print(f"XSS vulnerability detected with payload: {payload}")
            else:
                print(f"No vulnerability found for payload: {payload}")
        except requests.RequestException as e:
            print(f"Error during XSS attack: {e}")
