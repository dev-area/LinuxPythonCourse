
import struct
import termios

from common.protocol import (
    SOF,
    CMD_ALIVE,
    CMD_GET_SENSOR_VALUE,
    CMD_SET_SENSOR_LIMITS,
    STATUS_OK,
    STATUS_UNKNOWN_COMMAND,
    STATUS_INVALID_PAYLOAD,
    STATUS_SENSOR_NOT_FOUND,
    STATUS_CRC_ERROR,
    build_response,
    parse_message
)

SERIAL_PORT = "/dev/ttyAMA0"

# Temporary sensor data
sensors = {
    0: 255
}

sensor_limits = {
    0: (150, 350)
}


def handle_command(cmd, payload):

    if cmd == CMD_ALIVE:
        if len(payload) != 0:
            return build_response(cmd, STATUS_INVALID_PAYLOAD)

        return build_response(cmd, STATUS_OK)

    elif cmd == CMD_GET_SENSOR_VALUE:
        if len(payload) != 1:
            return build_response(cmd, STATUS_INVALID_PAYLOAD)

        sensor_id = payload[0]

        if sensor_id not in sensors:
            return build_response(cmd, STATUS_SENSOR_NOT_FOUND)

        data = struct.pack(">Bh", sensor_id, sensors[sensor_id])
        return build_response(cmd, STATUS_OK, data)

    elif cmd == CMD_SET_SENSOR_LIMITS:
        if len(payload) != 5:
            return build_response(cmd, STATUS_INVALID_PAYLOAD)

        sensor_id, lower, upper = struct.unpack(">Bhh", payload)

        if sensor_id not in sensors:
            return build_response(cmd, STATUS_SENSOR_NOT_FOUND)

        if lower > upper:
            return build_response(cmd, STATUS_INVALID_PAYLOAD)

        sensor_limits[sensor_id] = (lower, upper)
        print("New limits:", sensor_limits[sensor_id])

        return build_response(cmd, STATUS_OK)

    else:
        return build_response(cmd, STATUS_UNKNOWN_COMMAND)


def read_exact(serial, count):
    data = b""

    while len(data) < count:
        chunk = serial.read(count - len(data))

        if not chunk:
            raise ConnectionError("Serial connection closed")

        data += chunk

    return data


def receive_message(serial):
    # Find the start of a message
    while True:
        first = read_exact(serial, 1)

        if first == SOF[:1]:
            second = read_exact(serial, 1)

            if second == SOF[1:]:
                break

    # Read CMD and LEN
    header = read_exact(serial, 3)
    cmd = header[0]
    length = int.from_bytes(header[1:3], "big")

    # Read PAYLOAD and CRC
    body = read_exact(serial, length + 2)

    return SOF + header + body


print("Serial Binary Server is starting...")

with open(SERIAL_PORT, "r+b", buffering=0) as serial:

    # Disable terminal processing and echo
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

    print("Waiting for UART data...")

    while True:
        try:
            message = receive_message(serial)
            print("Received:", message.hex().upper())

            try:
                cmd, length, payload = parse_message(message)
                response = handle_command(cmd, payload)

            except ValueError as error:
                print("Protocol error:", error)

                # CRC error response
                cmd = message[2]
                response = build_response(cmd, STATUS_CRC_ERROR)

            serial.write(response)
            print("Response:", response.hex().upper())

        except ConnectionError as error:
            print("Serial error:", error)
            break
