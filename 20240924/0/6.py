a, b = eval(input())
print(*[i for i in range(a, b) if i % 2 and "3" not in str(i)])


