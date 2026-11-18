import socket
import os
import time
import select
import tty

# הגדרות TCP
TCP_HOST = "192.168.0.2"
TCP_PORT = 5000

# הגדרות UART
SERIAL_PORT = "/tmp/virtual-uart"

# פתיחת חיבור UART
serial_port = os.open(SERIAL_PORT, os.O_RDWR)
tty.setraw(serial_port)

print("Combined Client started")

while True:

    # יצירת חיבור TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3)
    client.connect((TCP_HOST, TCP_PORT))

    # שליחת PING ב-TCP
    client.sendall(b"PING")

    # קבלת תשובה מהשרת
    response = client.recv(1024)
    print("TCP received:", response)

    # סגירת חיבור TCP
    client.close()

    # שליחת PING ב-UART
    os.write(serial_port, b"PING\n")

    # המתנה לתשובה מהשרת
    ready, _, _ = select.select([serial_port], [], [], 2)

    if ready:
        response = os.read(serial_port, 1024)
        print("UART received:", response)
    else:
        print("UART: No response")

    # המתנה של 5 שניות
    time.sleep(5)