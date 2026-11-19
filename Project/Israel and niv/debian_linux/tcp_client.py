import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = 6004

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.settimeout(5)
    s.connect((HOST, PORT))    # TCP three-way handshake
    for text in ["hello", "sockets in python"]:
        s.sendall(text.encode())   # str -> bytes
        reply = s.recv(1024)
        print(f"{text!r} -> {reply.decode()!r}")