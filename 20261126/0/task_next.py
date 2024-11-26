import random
import struct

with open("1.bin", "wb") as f:
    for i in range(10):
        f.write(struct.pack("f3si", random.random(),
                            bytes ((random.randrange(2),
                                    random.randrange(2),
                                    random.randrange(2))),
                            random.randrange(25600)))