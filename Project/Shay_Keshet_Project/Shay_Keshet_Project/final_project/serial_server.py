SERIAL_PORT = "/dev/ttyAMA0"

print("Serial Server is starting...")

with open(SERIAL_PORT, "r+b", buffering=0) as serial:
    print("Waiting for UART data...")

    while True:
        data = serial.readline()
        message = data.decode().strip()

        print("Received:", message)

        response = "Hello from QEMU Python!\n"
        serial.write(response.encode())

        print("Response sent!")