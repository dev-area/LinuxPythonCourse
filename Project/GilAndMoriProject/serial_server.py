import os
import tty

PORT = "/dev/ttyAMA0"

serial_port = os.open(PORT, os.O_RDWR)

# Disable terminal processing and echo
tty.setraw(serial_port)

print("Serial Server started")

try:
    while True:

        message = os.read(serial_port, 1024)

        if b"PING" in message:
            print("Received PING")

            os.write(serial_port, b"PONG\n")

            print("Sent PONG")

except KeyboardInterrupt:
    print("\nServer stopped")

finally:
    os.close(serial_port)