a = list(range(5, 16))
b = []
for i in range(ord('a'), ord('k') + 1):
     b.append(chr(i))
a[4:8] = b[-5:]
print(*a)
