def gen(x):
    yield x
    yield x + 1
    yield "Done"

e = gen(2)
print(e, next(e))
for i in e:
    print(i)