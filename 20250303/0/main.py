import readline
import shlex
while s := input("command>  "):
	print(shlex.join(shlex.split(s)))


