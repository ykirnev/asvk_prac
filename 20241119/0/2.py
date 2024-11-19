def istype(tpe):
    def d(f):
        def newfun(*args):
            for i in args:
                if not isinstance(i, tpe):
                    raise TypeError
            return f(*args)
    return d


def genf(f):
    def newfun(*args):
        print(">", *args)
        res = f(*args)
        print("<", res)
        return res
    return newfun

@istype(str)
@genf
def fun(a, b):
    return a + b * 2
newf = genf(fun)


try:
    print(fun(2, 3))
except:
    print('TypeError')