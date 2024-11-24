import sys
def objcount(cls):
    cls.counter = 0
    or_init = getattr(cls, "__init__", None)
    def new_init(self, *args, **kwargs):
        cls.counter += 1
        if or_init:
            or_init(self, *args, **kwargs)
    cls.__init__ = new_init
    or_del = getattr(cls, "__del__", None)
    def new_del(self):
        cls.counter -= 1
        if or_del:
            or_del(self)
    cls.__del__ = new_del
    return cls
exec(sys.stdin.read())
