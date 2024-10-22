def f(x):
    yield "1"
    yield from x
    yield "2"
    return len(x)
print(list(f("qdeqefrevrb")))