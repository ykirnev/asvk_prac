C = type("C", (), {"a":100500, "fun": lambda self: self.a,
                   "__init__": lambda self, a:self.__setattr__("a", a)})
print(C)
c = C(1)
print(c.fun())
print(C(2).a)