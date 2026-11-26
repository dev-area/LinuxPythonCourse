#!/usr/bin/env python3
"""TCP client. Run on the DEBIAN host (192.168.0.1).
Usage: python3 tcp_client.py [server_ip] [port] [message]
"""
import socket
import sys

SERVER = sys.argv[1] if len(sys.argv) > 1 else "192.168.0.2"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 9000
MSG = (sys.argv[3] if len(sys.argv) > 3 else "hello tshark").encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER, PORT))
    s.sendall(MSG)
    data = s.recv(1024)
    print(f"sent:     {MSG!r}")
    print(f"received: {data!r}")
