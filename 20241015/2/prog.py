from math import *


def f(txt):
    funcs = {}
    num_funcs = 0
    cnt = 0
    for line in txt:
        cnt += 1
        if line.startswith(":"):
            a = line.split()
            func_name = a [0][1:]
            pars = a[1:-1]
            func = a[-1]
            func = f"lambda {', '.join(pars)}: {func}"
            funcs[func_name] = eval(func, globals())
        elif line.startswith("quit"):
            res = line[line.find('"') + 1:line.rfind('"')]
            res = res.format(num_funcs, cnt)
            print(res)
            break

        else:
            a = line.split()
            func_name = a[0]
            pars = a[1:]
            if func_name in funcs:
                num_funcs += 1
                pars = [eval(par) if par.isdigit() else par.replace('"', '') for par in pars]
                result = funcs[func_name](*pars)
                print(result)

txt = []
a = input()
while not (a.startswith("quit")):
    txt.append(a)
    a = input()
txt.append(a)
f(txt)