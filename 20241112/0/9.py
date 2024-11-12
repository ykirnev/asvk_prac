from math import inf


def divisor(a, b):
    c = a / b
    return -c

def proxy(fun, *args):
    try:
        return fun(*args)
    except ZeroDivisionError:
        return inf
for i in range(-2, 3):
    print(proxy(divisor, 100, i))
