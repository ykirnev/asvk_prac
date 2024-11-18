from collections import UserString
import sys
class DivStr(UserString):
    def __init__(self, seq=""):
        super().__init__(seq)

    def __floordiv__(self, n):
        ln = len(self.data) // n
        return (DivStr(self.data[i * ln:(i + 1) * ln]) for i in range(n))

    def __mod__(self, n):
        ln = len(self.data) // n
        return DivStr(self.data[n * ln:])

exec(sys.stdin.read())