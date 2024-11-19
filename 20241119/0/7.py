class C:
    @property
    def age(self):
        if self._v == 42:
            print("secret")
            return -1
        return self._v

    @age.setter
    def age(self, value):
        if value > 128:
            raise ValueError
        self._v = value

    @x.getter
    def x(self, value):
        self._x = value

