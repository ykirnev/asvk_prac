a = list(eval(input()))
n = len(a)
matrix1, matrix2 = [], []
matrix1.append(a)
for i in range(n - 1):
    a = list(eval(input()))
    matrix1.append(a)
for i in range(n):
    a = list(eval(input()))
    matrix2.append(a)
for i in range(n):
    for j in range(n):
        sum = 0
        for k in range(n):
            sum += matrix1[i][k] * matrix2[k][j]
        print(sum, end='')
        if j != n - 1: print('', end=',')
    print()

