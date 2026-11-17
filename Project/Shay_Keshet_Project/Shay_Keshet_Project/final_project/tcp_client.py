
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("192.168.0.2", 5000))

client.sendall(b"Hello from Debian!")

response = client.recv(1024)

print("Server response:", response.decode())

client.close()
