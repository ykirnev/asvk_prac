def pgen():
    print("Before")
    res = yield "Start"
    print(">")
    while res:= (yield f"/{res}/"):
        print(">")
    yield "Finish"
    print("<")
g = pgen()
print(next(g))
s = g.send(2121)
print(s)