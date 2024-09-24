from sympy import isprime
a, b = eval(input())
print([i for i in range(a, b) if isprime(i)])
