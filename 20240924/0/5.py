m = []
a = list(eval(input()))
m.append(a)
for i in range(1, len(a)):
    a = list(eval(input()))
    m.append(a)
for a in m:
    print(*a)
print()
for i in range(len(a)):
    for j in range(i, len(a)):
        m[i][j], m[j][i] = m[j][i], m[i][j]
for a in m:
    print(*a)


