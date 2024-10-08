from math import *
def scale(a, b, A, B, x):
    return A + (x - a) * (B - A) / (b - a)
W = 60
H = 20
a, b = -4, 4
for i in range(H):
    x = (b - a) / (H - 1) * i + a
    x = scale(0, H - 1, a, b, i)
    y = sin(x)
    shift = round(scale(-1, 1, 0, W - 1, y))
    print(" " * shift, "*")




