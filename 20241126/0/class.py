import pickle
class SerCls():
    def __init__(self, lst = [], dct ={}, num = 0, st = ''):
        self.lst = lst
        self.dct = dct
        self.num = num
        self.st = st
    def __str__(self):
        return f"{self.lst}, {self.dct}, {self.num}, {self.st}"

ser = SerCls([2, 0, 2, 4], {0:1, 1:2}, 2024, "qwqwqwqw")
print(ser)
dump = pickle.dumps(ser)
del ser
serl = pickle.loads(dump)
print(serl)