import socket

server_ip = '192.233.233.2'  # Ganti dengan IP server 
server_port = 0000           # Ganti dengan port yang Anda tentukan

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((server_ip, server_port))
server.listen(5) 

print(f"Server berjalan di {server_ip}:{server_port}...")

while True:
    client, address = server.accept()
    print(f"Koneksi diterima dari {address}")

    while True:
        try:
            data = client.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Data diterima: {data}")
            
            response = "Data diterima"
            client.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break

    client.close()
    print(f"Koneksi dari {address} ditutup")
