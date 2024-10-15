from collections import Counter
import timeit

def dict_cnt(txt):
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
    return cnt

def dict_cnt_Counter(txt):
    return sum(i for i in Counter(txt.split()).values() if i == 1)

txt = ''
while a := input():
    txt += a
print("Dict_cnt",timeit.Timer("dict_cnt(txt)", globals=globals()).autorange())
print("Counter",timeit.Timer("dict_cnt_Counter(txt)", globals=globals()).autorange())