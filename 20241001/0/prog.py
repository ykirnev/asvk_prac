from math import*
def fun(a, *args, def1=123):
    print(a, args, def1)


fun(1, def1=100500)


def average(*args):
    if len(args) != 0:
        return sum(args) / len(args)
    return 0


print(average(1, 2, 3, 4, 5, 6))
print(average(*range(100)))
fun = lambda x, y: x * 2 + y
print(sorted(range(20), key=lambda x: x % 5))
print(*sorted(eval(input()), key=lambda x: x * x % 100))

def fun(n):
    return fun(n - 1) if n > 0 else 1
fun(5)

def minf(*funcs):
    def answer(x):
        mn = funcs[0](x)
        for i in range(1, len(funcs)):
            mn = min (mn, funcs[i](x))
        return mn
    return answer
print(minf(sin, cos, tan)(pi))

def S(f, g):
    def fun(x):
        return f(x) + g(x)
    return fun
print(S(sin, cos)(1))

def F():
    x = 2
    def fun():
        return x
    print(fun.__closure__[0].cell_contents)
    x = 3
    print(fun.__closure__[0].cell_contents)
    return fun
res = F()
print(res())

def F(a, b):
    def func(x):
        return a * x + b
    return func
print(F(1, 2)(5))

print("______")
def rbin(n, i = 1):
    if n < 0:
        return 0
    if (len(bin(i)) == (n + 2)):
        print(bin(i)[2:])
    else:
        rbin(n, i << 1)
        rbin(n, i << 1 | 1)
rbin(3)

