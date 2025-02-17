import zlib
from pathlib import Path
ob = Path(".git/objects/d5/7a6a231d2664e8491a4f945f86251587fdbb55").read_bytes()
obb = zlib.decompress(ob)
print(obb)
header, _, body = obb.partition(b'\x00')
print(header, body)