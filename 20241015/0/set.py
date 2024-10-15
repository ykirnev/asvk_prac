import timeit

def checker(s):
    def is_g(s):
        return s in 'eyuoia'
    def is_s(s):
        return s in 'qwrtpsdfghjklzxcvbnm'
    gl = {i for i in s if is_g(i) and i.islower()}
    sg = {i for i in s if is_s(i) and i.islower()}
    print(gl, sg)
s = input()
print(timeit.Timer("checker(s)", globals=globals()).autorange())