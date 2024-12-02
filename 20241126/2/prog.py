import sys

txt = sys.stdin.read()
dec = txt.encode("latin1", errors="replace").decode("cp1251", errors="replace")
sys.stdout.write(dec)
