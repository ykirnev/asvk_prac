class Dumper():
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        def newfun(*args):
            if not all(isinstance(arg, self.function) for arg in args):
                raise TypeError
            return fun(*args)
        return newfun

def istype(tpe):
    def d(f):
        def newfun(*args):
            for i in args:
                if not isinstance(i, tpe):
                    raise TypeError
            return f(*args)
    return d

@istype(int)
def fun(a, b):
    return a + b * 2


a = Dumper(fun(2, 3))
try:
    print(fun(2, 3))
except:
    print('TypeError')