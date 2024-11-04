from itertools import product
print(*sorted(filter(lambda s: s.count("TOR") == 2, map("".join, product("TOR", repeat=int(input()))))), sep = ', ')