def isint(f):
    def newfun(*args):
        for i in args:
            if type(i) != int:
                raise TypeError
    return f


def genf(f):
    def newfun(*args):
        print(">", *args)
        res = f(*args)
        print("<", res)
        return res
    return newfun

@isint
@genf
def fun(a, b):
    return a + b * 2
newf = genf(fun)


try:
    print(fun(2, 3))
except:
    print('TypeError')