import os
import time
import select
import tty

PORT = "/tmp/virtual-uart"

serial_port = os.open(PORT, os.O_RDWR)

# Disable terminal processing and echo
tty.setraw(serial_port)

print("Serial Client started")

try:
    while True:

        os.write(serial_port, b"PING\n")
        print("Sent PING")

        # Wait up to 2 seconds for a response
        ready, _, _ = select.select([serial_port], [], [], 2)

        if ready:
            response = os.read(serial_port, 1024)

            if response.strip() == b"PONG":
                print("QEMU replied: PONG")
            else:
                print("Unexpected data received")
        else:
            print("No response from QEMU")

        time.sleep(5)

except KeyboardInterrupt:
    print("\nClient stopped")

finally:
    os.close(serial_port)