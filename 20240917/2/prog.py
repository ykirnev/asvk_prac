x = int(input())
sum = 0
while (x > 0):
    sum += x
    if (sum > 21):
        print(sum)
        break
    x = int(input())
else:
    print(x)
