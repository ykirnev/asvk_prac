import binascii
with open("1.bin", 'rb' ) as f:
    data = f.read()
print(len(data))
print(binascii.hexlify(data, "\n", 16).decode())
mas = binascii.hexlify(data, " ", 4).decode().split()
for ad, i in enumerate(range(0, len(mas), 4)):
    print(f"{ad:08x}", ":", *mas[i : i + 4])