class Rectangle:
    rectcnt = 0
    def __init__(self, x1, y1, x2, y2):
        Rectangle.rectcnt += 1
        self.__setattr__("rect_" + str(Rectangle.rectcnt), 0)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
    def __str__(self):
        return f'{self.x1, self.y1}{self.x1, self.y2}{self.x2, self.y1}{self.x2, self.y2}'
    def square(self):
        return abs(self.x1 - self.x2) * abs(self.y1 - self.y2)
    def __lt__(self, other):
        return self.square() < other.square()
    def __eq__(self, other):
        return self.square() == other.square()
    def __mul__(self, n):
        return Rectangle(self.x1 * n, self.y1 * n, self.x2 * n, self.y2 * n)
    def __rmul__(self, n):
        return Rectangle(n * self.x1, n * self.y1, n * self.x2, n * self.y2)
    def __getitem__(self, id):
        mas = [(self.x1, self.y1), (self.x1, self.y2), (self.x2, self.y1), (self.x2, self.y2)]
        return mas[id]
    def __bool__(self):
        return self.square() != 0
    def __del__(self):
        self.rectcnt -= 1
        print(f"rectcnt; {Rectangle.rectcnt}")

a = Rectangle(1, 2, 3, 4)
b = Rectangle(2, 2, 3, 4)
print(a == b)
c = Rectangle(1, 2, 3, 4)
d = Rectangle(1, 2, 3, 2)
print(a)
print(Rectangle.rectcnt)
print(a.__dict__)
print(a * 3, 5 * a)
print(a[2], c[-2])
print(a.__bool__(), d.__bool__())
