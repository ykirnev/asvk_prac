n = int(input())
i, j = 0, 0
while i < 3:
    j = 0
    while j < 3:
        print(n + i, '*', n + j, '=', end= ' ')
        x = (n + j) * (n + i)
        sum = 0
        while x > 0:
            sum += x % 10
            x //= 10
        if sum == 6:
            print(':=)', end=' ')
        else:
            print((n + j) * (n + i), end=' ')
        j += 1
    i += 1
    print()
