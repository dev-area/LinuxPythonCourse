import socket

# QEMU IP and port
HOST = "0.0.0.0"
PORT = 5000

# Create TCP socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Allow reuse of the port
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind server to IP and port
server.bind((HOST, PORT))

# Start listening for connections
server.listen(1)

print("TCP Server is waiting for connection...")

try:
    while True:

        # Wait for client
        client, address = server.accept()

        print("Client connected:", address)

        # Receive message
        message = client.recv(1024)

        print("Received:", message.decode())

        # Send response
        client.sendall(b"PONG")

        print("Sent PONG")

        # Close client connection
        client.close()

except KeyboardInterrupt:
    print("\nServer stopped")

finally:
    server.close()