def gen():
    sm = 0
    i = 1
    while True:
        sm += 1/(i * i)
        i += 1
        yield sm
e = gen()
for i in e:
    print(next(e))