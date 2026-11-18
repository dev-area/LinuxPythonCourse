
import struct
import termios

from common.protocol import (
    CMD_ALIVE,
    CMD_GET_SENSOR_VALUE,
    CMD_SET_SENSOR_LIMITS,
    build_message,
    parse_message
)

SERIAL_PORT = "/tmp/virtual-uart"


def read_exact(serial, count):
    data = b""

    while len(data) < count:
        chunk = serial.read(count - len(data))

        if not chunk:
            raise ConnectionError("Serial connection closed")

        data += chunk

    return data


def send_command(serial, cmd, payload=b""):
    request = build_message(cmd, payload)

    serial.write(request)
    print("Sent:", request.hex().upper())

    # Read SOF, CMD and LEN
    header = read_exact(serial, 5)

    length = int.from_bytes(header[3:5], "big")

    # Read PAYLOAD and CRC
    body = read_exact(serial, length + 2)

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


with open(SERIAL_PORT, "r+b", buffering=0) as serial:

    # Configure the serial port for binary data
    settings = termios.tcgetattr(serial.fileno())
    settings[0] = 0
    settings[1] = 0
    settings[3] = 0
    settings[6][termios.VMIN] = 1
    settings[6][termios.VTIME] = 0
    termios.tcsetattr(
        serial.fileno(),
        termios.TCSANOW,
        settings
    )

    print("\n--- SERIAL ALIVE ---")
    status, data = send_command(serial, CMD_ALIVE)

    print("\n--- SERIAL GET SENSOR VALUE ---")
    status, data = send_command(
        serial,
        CMD_GET_SENSOR_VALUE,
        struct.pack(">B", 0)
    )

    if status == 0:
        sensor_id, value = struct.unpack(">Bh", data)
        print("Sensor:", sensor_id)
        print("Value:", value)

    print("\n--- SERIAL SET SENSOR LIMITS ---")
    status, data = send_command(
        serial,
        CMD_SET_SENSOR_LIMITS,
        struct.pack(">Bhh", 0, 150, 350)
    )

    if status == 0:
        print("Sensor limits updated successfully!")
