def travel(n):
    i = 0
    while i < n:
        i += 1
        yield "по кочкам"
    return "ЯМАААА"

def travelwrap(n):
    story = yield from travel(n)
    yield story

print(list(travelwrap(10)))