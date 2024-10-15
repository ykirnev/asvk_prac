s = input()
m = dict()
for i in range(len(s) - 1):
    tmp = s[i:i + 2].lower()
    if tmp[0].isalpha() and tmp[1].isalpha():
        m[tmp] = 1
print(len(m))