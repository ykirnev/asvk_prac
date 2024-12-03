
while(s:=input('> ')):
    match s.split():
        case['mov', r1, r2]:
            print(f"moving {r2} to {r1}")
        case[('push' as cmd) | ('pop' as cmd), *args]:
            print(f"{cmd}ing",  *args)
        case[cmd, r]:
            print(f"making {cmd} with {r}")
        case _:
            print("Parse error")
