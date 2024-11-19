import sys
from string import ascii_letters
from pympler.asizeof import asizeof
class Trad:
    def __init__(self):
        for attr in ascii_letters:
            setattr(self, attr, attr)

class Slotter:
    __slots__ = tuple(ascii_letters)

    def __init__(self):
        for attr in ascii_letters:
            setattr(self, attr, attr)

a = Slotter()
print(sys.getsizeof(a))
print('a', asizeof(a))
a = Trad()
print(sys.getsizeof(a))
print('a', asizeof(a))

a = [Trad() for i in range(1000)]
print(sys.getsizeof(a))
print('a', asizeof(a))

a = [Slotter() for i in range(1000)]
print(sys.getsizeof(a))
print('a', asizeof(a))