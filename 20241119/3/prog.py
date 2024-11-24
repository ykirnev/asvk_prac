import sys


class Vowel:
    __slots__ = ('a', 'o', 'u', 'i', 'e', 'y')
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.__slots__:
                setattr(self, key, value)
            else:
                raise AttributeError

    def __str__(self):
        sorted_fields = sorted(
            (key for key in self.__slots__ if hasattr(self, key)),
            key=lambda k: k
        )
        return ', '.join(f'{key}: {getattr(self, key)}' for key in sorted_fields)

    @property
    def answer(self):
        return 42

    @answer.setter
    def answer(self, value):
        raise AttributeError

    @property
    def full(self):
        return all(hasattr(self, key) for key in self.__slots__)

    @full.setter
    def full(self, value):
        pass

exec(sys.stdin.read())