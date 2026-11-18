
import socket
import struct

from common.protocol import (
    CMD_ALIVE,
    CMD_GET_SENSOR_VALUE,
    CMD_SET_SENSOR_LIMITS,
    build_message,
    parse_message
)

HOST = "192.168.0.2"
PORT = 5000


def send_command(cmd, payload=b""):
    # Connect to QEMU server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.settimeout(5)
        client.connect((HOST, PORT))

        # Build and send binary request
        request = build_message(cmd, payload)
        client.sendall(request)

        print("Sent:", request.hex().upper())

        # Receive complete response header
        header = b""

        while len(header) < 5:
            chunk = client.recv(5 - len(header))
            if not chunk:
                raise ConnectionError("Connection closed")
            header += chunk

        # Receive payload and CRC
        length = int.from_bytes(header[3:5], "big")
        body = b""

        while len(body) < length + 2:
            chunk = client.recv(length + 2 - len(body))
            if not chunk:
                raise ConnectionError("Connection closed")
            body += chunk

        response = header + body
        print("Received:", response.hex().upper())

        response_cmd, _, response_payload = parse_message(response)

        if response_cmd != (cmd | 0x80):
            raise ValueError("Unexpected response command")

        if len(response_payload) < 1:
            raise ValueError("Missing STATUS")

        status = response_payload[0]
        data = response_payload[1:]

        print("STATUS:", status)

        return status, data


# TEST 1 - ALIVE
print("\n--- ALIVE ---")
status, data = send_command(CMD_ALIVE)

# TEST 2 - GET SENSOR VALUE
print("\n--- GET SENSOR VALUE ---")
sensor_id = 0
status, data = send_command(
    CMD_GET_SENSOR_VALUE,
    struct.pack(">B", sensor_id)
)

if status == 0:
    sensor, value = struct.unpack(">Bh", data)
    print("Sensor:", sensor)
    print("Value:", value)

# TEST 3 - SET SENSOR LIMITS
print("\n--- SET SENSOR LIMITS ---")
status, data = send_command(
    CMD_SET_SENSOR_LIMITS,
    struct.pack(">Bhh", 0, 150, 350)
)

if status == 0:
    print("Sensor limits updated successfully!")
