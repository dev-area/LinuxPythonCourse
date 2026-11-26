#!/usr/bin/env python3
"""Simple UDP echo server. Run on the QEMU guest (192.168.0.2)."""
import socket

HOST = "0.0.0.0"
PORT = 9001

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    print(f"UDP server listening on {HOST}:{PORT}")
    while True:
        data, addr = s.recvfrom(1024)
        print(f"got {len(data)} bytes from {addr}")
        s.sendto(data, addr)  # echo back
