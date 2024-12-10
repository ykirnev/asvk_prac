def subr(n):
    x = yield f"({n}) Wait for x"
    y = yield f"({n}) Wait for y ({x=})"
    return x, y

def task(n):
    while True:
        value = yield from subr(n)
        _ = yield f"[{n}]: {value}"

cores = task(0), task(1)
print(next(cores[0]), next(cores[1]), sep="\n")
for i in range(20):
    print(cores[not i % 3].send(i))