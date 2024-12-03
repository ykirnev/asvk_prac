class C:
    a: int
    def __init__(self, val):
        if type(val) != self.__class__.__annotations__["a"]:
            print("Unlucky")
            return
        self.a = val

c = C(1)
c = C("1")