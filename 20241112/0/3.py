class A:
    __v = 0
    def inc(self):
        self.__v += 1
        print(self.__v)
class B(A):
    __v = 100500

b = B()
b.inc()
b.inc()
print(b._B__v, b._A__v)
