
SOF = bytes.fromhex("AA55")

# Commands
CMD_ALIVE = 0x01
CMD_GET_SENSOR_VALUE = 0x02
CMD_SET_SENSOR_LIMITS = 0x03

# Status codes
STATUS_OK = 0
STATUS_UNKNOWN_COMMAND = 1
STATUS_CRC_ERROR = 2
STATUS_INVALID_PAYLOAD = 3
STATUS_SENSOR_NOT_FOUND = 4
STATUS_INTERNAL_ERROR = 5


def calculate_crc(data):
    crc = 0xFFFF

    for byte in data:
        crc ^= byte << 8

        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc = crc << 1

            crc &= 0xFFFF

    return crc


def build_message(cmd, payload=b""):
    length = len(payload).to_bytes(2, byteorder="big")

    message_data = bytes([cmd]) + length + payload

    crc_value = calculate_crc(message_data)
    crc_bytes = crc_value.to_bytes(2, byteorder="big")

    return SOF + message_data + crc_bytes


def parse_message(message):
    if len(message) < 7:
        raise ValueError("Message too short")

    if message[:2] != SOF:
        raise ValueError("Invalid SOF")

    cmd = message[2]
    length = int.from_bytes(message[3:5], byteorder="big")

    if len(message) != 7 + length:
        raise ValueError("Invalid message length")

    payload = message[5:5 + length]

    received_crc = int.from_bytes(
        message[5 + length:7 + length],
        byteorder="big"
    )

    calculated_crc = calculate_crc(message[2:5 + length])

    if received_crc != calculated_crc:
        raise ValueError("CRC Error")

    return cmd, length, payload


def build_response(cmd, status=STATUS_OK, data=b""):
    response_cmd = cmd | 0x80
    response_payload = bytes([status]) + data

    return build_message(response_cmd, response_payload)


if __name__ == "__main__":
    print("CRC test:", hex(calculate_crc(b"123456789")))

    message = build_message(CMD_ALIVE)
    print("ALIVE request:", message.hex().upper())

    cmd, length, payload = parse_message(message)
    print("Request CMD:", cmd)

    response = build_response(CMD_ALIVE)
    print("ALIVE response:", response.hex().upper())

    response_cmd, response_length, response_payload = parse_message(response)
    print("Response CMD:", hex(response_cmd))
    print("Response STATUS:", response_payload[0])
