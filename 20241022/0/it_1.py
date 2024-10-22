from itertools import filterfalse
def f(mod, seq):
    return filterfalse(lambda x: x % mod ,seq)
