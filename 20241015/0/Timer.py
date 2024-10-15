import timeit
s = input()
print(timeit.Timer(eval(s)).autorange())