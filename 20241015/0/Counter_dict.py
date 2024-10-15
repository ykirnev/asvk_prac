from collections import Counter
txt = ''
while a:=input():
    txt += a
print(sum(i for i in Counter(txt.split()).values() if i == 1))