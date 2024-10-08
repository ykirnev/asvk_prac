from fractions import Fraction as frac
mas = list(map(frac, input().split(',')))
s = mas[0]
w = mas[1]
a_degree = mas[2]
a_x = 0
for i in range(1, int(a_degree) + 2):
    a_x = a_x * s + mas[i + 2]
b_degree = mas[i + 3]
b_x = 0
for j in range(i + 4, i + 3 + int(b_degree) + 2):
    b_x = b_x * s + mas[j]
print(frac(a_x, b_x) == w)