import sys
with open(sys.argv[1]) as f:
    text = f.read()
for i in range(len(text) // 3, len(text)):
    if text[i] == '\n':
        break
else:
    i +=1

print(text[:i])