
import socket
import struct

from common.protocol import (
    CMD_ALIVE,
    CMD_GET_SENSOR_VALUE,
    CMD_SET_SENSOR_LIMITS,
    STATUS_OK,
    STATUS_UNKNOWN_COMMAND,
    STATUS_INVALID_PAYLOAD,
    STATUS_SENSOR_NOT_FOUND,
    build_response,
    parse_message
)

HOST = "0.0.0.0"
PORT = 5000

# Temporary sensor data for testing
sensors = {
    0: 255
}

# Sensor limits
sensor_limits = {
    0: (150, 350)
}


def handle_command(cmd, payload):

    # Command 1: ALIVE
    if cmd == CMD_ALIVE:
        if len(payload) != 0:
            return build_response(cmd, STATUS_INVALID_PAYLOAD)

        return build_response(cmd, STATUS_OK)

    # Command 2: GET SENSOR VALUE
    elif cmd == CMD_GET_SENSOR_VALUE:
        if len(payload) != 1:
            return build_response(cmd, STATUS_INVALID_PAYLOAD)

        sensor_id = payload[0]

        if sensor_id not in sensors:
            return build_response(cmd, STATUS_SENSOR_NOT_FOUND)

        sensor_value = sensors[sensor_id]

        response_data = struct.pack(">Bh", sensor_id, sensor_value)

        return build_response(cmd, STATUS_OK, response_data)

    # Command 3: SET SENSOR LIMITS
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

    # Unknown command
    else:
        return build_response(cmd, STATUS_UNKNOWN_COMMAND)


def receive_message(conn):
    # Read exactly the 5-byte header
    header = b""

    while len(header) < 5:
        chunk = conn.recv(5 - len(header))

        if not chunk:
            raise ConnectionError("Connection closed")

        header += chunk

    # Read the payload and CRC
    length = int.from_bytes(header[3:5], "big")
    remaining = length + 2
    body = b""

    while len(body) < remaining:
        chunk = conn.recv(remaining - len(body))

        if not chunk:
            raise ConnectionError("Connection closed")

        body += chunk

    return header + body


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print("TCP Binary Server is running...")

while True:
    conn, addr = server.accept()
    print("Client connected:", addr)

    with conn:
        try:
            data = receive_message(conn)
            print("Received:", data.hex().upper())

            cmd, length, payload = parse_message(data)

            response = handle_command(cmd, payload)

            conn.sendall(response)
            print("Response:", response.hex().upper())

        except (ValueError, ConnectionError) as error:
            print("Protocol error:", error)

server.close()
