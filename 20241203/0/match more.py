v_1, v_2, v_3 = input().split()
while s:= input():
    match s.split():
        case[f_1, *args] if 'yes' in args and v_1 == f_1:
            print("1")
        case[f_2] if f_2 == v_2:
            print(2)
        case[f_3, *args, f_2] if f_3 == v_3 and v_2 == f_2:
            print(3)
        case _:
            print("Bananov")
