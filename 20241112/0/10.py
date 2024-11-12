EPS = 2

def divisor(a, b):
    if (abs(b) < EPS):
        raise ValueError("ALAAAARM")
    c = a / b
    return -c

def proxy(i):
    try:
        c = divisor(100, i)
        print(c)
    except ValueError as Q:
        print(*Q.args)


for i in range(-5, 5):
    proxy(i)