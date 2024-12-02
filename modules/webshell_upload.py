class WebShellUpload:
    def __init__(self):
        pass

    def upload_webshell(self, url):
        payload = "<script>alert('WebShell uploaded!')</script>"
        webshell_url = f"{url}?input={payload}"
        print(f"WebShell uploaded at: {webshell_url}")
        return webshell_url
