import re
from collections import Counter
W = int(input())
txt = ''
while a:=input():
    txt += a
txt = re.sub(r'[^a-zA-Zа-яА-Я]', ' ', txt)
words = txt.lower().split()
res = Counter([word for word in words if len(word) == W])
if res:
    max_count = max(res.values())
    max_words = [word for word, count in res.items() if count == max_count]
    max_words.sort()
    print(' '.join(max_words))