import sys
txt = sys.stdin.buffer.read()
N = txt[0]
tail = txt[1:]
L = len(tail)
mas = [tail[round(i * L / N): round((i + 1) * L / N)] for i in range(N)]
mas.sort()
s = b"".join(mas)
sys.stdout.buffer.write(bytes([N]) + s)
