from math import *
def show(screen):
    print("\n".join(["".join(s) for s in screen]))
def scale(a, b, A, B, x):
    return A + (x - a) * (B - A) / (b - a)
W, H = 200, 20
screen = [[" "] * W for i in range(H)]
a, b = -10, 10
for i in range(W):
    x = (b - a) / (W - 1) * i + a
    x = scale(0, W - 1, a, b, i)
    y = sin(x)
    shift = round(scale(-1, 1, 0, H - 1, y))
    screen[shift][i] = '*'
show(screen)