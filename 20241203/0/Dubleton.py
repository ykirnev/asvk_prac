class Doubeleton(type):
    _first = None
    _second = None
    flag = True
    def __call__(cls, *args, **kw):
        if cls._first is None:
             cls._first = super().__call__(*args, **kw)
        elif cls._second is None:
            cls._second = super().__call__(*args, **kw)
        if cls.flag:
            cls.flag = not cls.flag
            return cls._first
        else:
            cls.flag = not cls.flag
            return cls._second

class C(metaclass=Doubeleton): pass
print(*(C() for i in range(7)), sep="\n")

