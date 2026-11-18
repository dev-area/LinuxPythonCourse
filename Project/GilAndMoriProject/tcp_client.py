import socket
import time

# כתובת ה-IP של QEMU
HOST = "192.168.0.2"

# הפורט שעליו השרת מאזין
PORT = 5000

print("TCP Client started")

try:
    while True:

        try:
            # יצירת חיבור TCP
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # הגבלת זמן ההמתנה ל-3 שניות
            client.settimeout(3)

            # התחברות לשרת ב-QEMU
            client.connect((HOST, PORT))

            # שליחת הודעה לשרת
            client.sendall(b"PING")

            print("Sent PING")

            # קבלת תשובה מהשרת
            response = client.recv(1024)

            if response == b"PONG":
                print("QEMU replied: PONG")
            else:
                print("Unexpected response")

        except (OSError, socket.timeout):
            print("No connection to QEMU")

        finally:
            # סגירת החיבור
            client.close()

        # המתנה של 5 שניות לפני הבקשה הבאה
        time.sleep(5)

except KeyboardInterrupt:
    print("\nClient stopped")