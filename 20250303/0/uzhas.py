import shlex
f = input("ФИО: ")
m = input("Место: ")
res = shlex.join(["register", f, m])
print(res)
print(shlex.split(res))

