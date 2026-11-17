"""
zlib.py - pure-Python stand-in for the missing zlib module on the board.
Provides adler32, compress, decompress (stored blocks only).
Workaround until the board image is rebuilt with zlib.
"""
import struct

__version__ = "shim-1.0"
ZLIB_VERSION = "shim"
MAX_WBITS = 15
DEFLATED = 8
Z_DEFAULT_COMPRESSION = -1


class error(Exception):
    pass


def adler32(data, value=1):
    a = value & 0xFFFF
    b = (value >> 16) & 0xFFFF
    for byte in bytes(data):
        a = (a + byte) % 65521
        b = (b + a) % 65521
    return (b << 16) | a


def crc32(data, value=0):
    import binascii
    return binascii.crc32(data, value)


def compress(data, level=-1, wbits=MAX_WBITS):
    data = bytes(data)
    out = bytearray(b"\x78\x01")
    blocks = [data[i:i + 65535] for i in range(0, len(data), 65535)] or [b""]
    for i, block in enumerate(blocks):
        final = 1 if i == len(blocks) - 1 else 0
        n = len(block)
        out.append(final)
        out += struct.pack("<HH", n, n ^ 0xFFFF)
        out += block
    out += struct.pack(">I", adler32(data))
    return bytes(out)


def decompress(data, wbits=MAX_WBITS, bufsize=0):
    data = bytes(data)
    if len(data) < 6 or (data[0] & 0x0F) != 8:
        raise error("invalid zlib header")
    pos, out = 2, bytearray()
    while True:
        if pos >= len(data):
            raise error("truncated stream")
        header = data[pos]
        if (header >> 1) & 0x03 != 0:
            raise error("compressed data not supported by this shim")
        n, nc = struct.unpack("<HH", data[pos + 1:pos + 5])
        if n ^ 0xFFFF != nc:
            raise error("bad stored block")
        out += data[pos + 5:pos + 5 + n]
        pos += 5 + n
        if header & 1:
            break
    if struct.unpack(">I", data[pos:pos + 4])[0] != adler32(out):
        raise error("adler32 mismatch")
    return bytes(out)
