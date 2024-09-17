while a := input():
    if (eval(a) % 2 == 0):
        print(a)
    if (eval(a) == 13):
        print("Unlucky")
        break
else:
    print("Сongrats")
