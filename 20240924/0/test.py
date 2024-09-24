import sys
from random import randrange
n = int(sys.argv[1])
for i in range(n):
    print([randrange(10) for i in range(n)])
print()
