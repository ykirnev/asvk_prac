from math import *
def Calc(s, t, u):
    def func(x):
        return eval(u, {"x": eval(s), "y": eval(t)})
    return func
s, t, u = input().replace('"', "").split(',')
x = eval(input())
F = Calc(s, t, u)
result = F(x)
print(result)