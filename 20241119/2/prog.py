import sys

class Num:
    def __init__(self, value=0):
        self.value = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.value, 0)

    def __set__(self, instance, value):
        if isinstance(value, (int, float)):
            instance.__dict__[self.value] = value
        elif hasattr(value, '__len__'):
            instance.__dict__[self.value] = len(value)

exec(sys.stdin.read())
