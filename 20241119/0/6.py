
class Counter():
    def __init__(self):
        self.counter = 0

    def __get__(self, obj, cls):
        return self.counter

    def __set__(self, obj, val):
        self.counter = val

    def __delete__(self, obj):
        self.counter -= 1


class C:
    counter = Counter()
    def __init__(self):
        self.counter += 1
    def __del__(self):
        self.counter -= 1
c = C()
print(c.counter)
d = C()
print(d.counter)
del c
print(d.counter)