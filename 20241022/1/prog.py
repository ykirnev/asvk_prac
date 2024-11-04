def fib(m, n):
    a, b = 1, 1
    for i in range(m):
        a, b = b, a + b
    for i in range(n):
        yield a
        a, b = b, a + b
a = eval(input())