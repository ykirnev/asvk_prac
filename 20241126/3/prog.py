import struct
import sys
def parser():
    txt = sys.stdin.buffer.read()
    header = txt[:44]
    if len(header) < 44:
        return "NO"
    riff, file_size, wave = struct.unpack('<4sI4s', header[:12])
    if riff != b'RIFF' or wave != b'WAVE':
        return "NO"
    fmt, fmt_l, typ, chan_n, rate, smth_1, smth_2, bits = struct.unpack('<4sIHHIIHH', header[12:36])
    data, data_size = struct.unpack('<4sI', header[36:44])
    if fmt != b'fmt ' or data != b'data':
        return "NO"
    return f"Size={file_size}, Type={typ}, Channels={chan_n}, Rate={rate}, Bits={bits}, Data size={data_size}"

print(parser())
