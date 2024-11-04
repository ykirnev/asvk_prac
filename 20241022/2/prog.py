from itertools import islice, tee


def slide(seq, n):
    it = tee(seq, n)
    for i, j in enumerate(it):
        next(islice(j, i, i), None)
    for gap in zip(*it):
        yield from gap
    seq = list(seq)
    for i in range(1, n):
        yield from seq[-(n - i):]

a = eval(input())
