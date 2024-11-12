class A:
    pass
class B:
    pass
class C(A, B):
    pass
class D(A, B):
    pass
class E1(C, B):
    pass
class E2(C, A):
    pass
class E3(C, D):
    pass
class E4(D, C):
    pass
