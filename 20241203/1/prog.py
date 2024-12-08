import sys
class dump(type):
    def __new__(cls, name, bases, dct):
        new_dct = {}
        for name, val in dct.items():
            if callable(val):
                def make(method_name, method):
                    def fun(self, *args, **kwargs):
                        print(f"{method_name}: {args}, {kwargs}")
                        return method(self, *args, **kwargs)
                    return fun
                new_dct[name] = make(name, val)
            else:
                new_dct[name] = val
        return super().__new__(cls, name, bases, new_dct)

exec(sys.stdin.read())
