def example(value):
    match value:
        case 1:
            print("First case")
        case 1:
            print("Second case")
example(1)

C = type("C", (), {"f":123})
print(C, C.f)

C = type('C', (), {'var': 0, '__init__': lambda self, x: setattr(self,"var", x)})
print(C(100500).var)


