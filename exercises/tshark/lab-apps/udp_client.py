#!/usr/bin/env python3
"""UDP client. Run on the DEBIAN host (192.168.0.1).
Usage: python3 udp_client.py [server_ip] [port] [message]
"""
import socket
import sys

SERVER = sys.argv[1] if len(sys.argv) > 1 else "192.168.0.2"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 9001
MSG = (sys.argv[3] if len(sys.argv) > 3 else "hello udp").encode()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.settimeout(3.0)
    s.sendto(MSG, (SERVER, PORT))
    try:
        data, addr = s.recvfrom(1024)
        print(f"received: {data!r} from {addr}")
    except socket.timeout:
        print("timeout: no response (this is normal for UDP when nothing replies)")
