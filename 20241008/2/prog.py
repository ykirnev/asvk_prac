from math import *

def scale(a, b, A, B, x):
    return A + (x - a) * (B - A) / (b - a)

def show(screen):
    for row in reversed(screen):
        print("".join(row))
W, H, A, B, func = map(str, input().split())
W, H, A, B = int(W), int(H), float(A), float(B)
screen = [[" "] * W for i in range(H)]
samples = 100
x_values = [A + i * (B - A) / (samples - 1) for i in range(samples)]
y_values = [eval(func) for x in x_values]
min_y, max_y = min(y_values), max(y_values)
prev_y_pixel = None
for i in range(W):
    x = scale(0, W - 1, A, B, i)
    y = eval(func)
    y_pixel = round(scale(min_y, max_y, 0, H - 1, y))
    if 0 <= y_pixel < H:
        screen[y_pixel][i] = '*'
    if prev_y_pixel is not None:
        for j in range(min(y_pixel, prev_y_pixel), max(y_pixel, prev_y_pixel) + 1):
            screen[j][i - 1] = '*'
    prev_y_pixel = y_pixel
show(screen)