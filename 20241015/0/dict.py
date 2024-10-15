txt = ''
while a:=input():
    txt += a
d = {}
for i in txt.split():
    if i in d:
        d[i] += 1
    else:
        d[i] = 1
cnt = 0
for i in d:
    if d[i] == 1:
        cnt += 1
print(cnt)