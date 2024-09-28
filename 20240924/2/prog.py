a = list(eval(input()))
keys = []
n = len(a)
for i in range(n):
    keys.append(a[i] ** 2 % 100)
for i in range(n - 1):
    for j in range(n - 1 - i):
        if keys[j] > keys[j + 1]:
            keys[j], keys[j + 1] = keys[j + 1], keys[j]
            a[j], a[j + 1] = a[j+1], a[j]
print(a)




