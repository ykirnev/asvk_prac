match eval(input()):
    case 1:
        print("один")
    case 2:
        print("два")
    case 3:
        print("три")
    case var if var % 2 == 0:
        print("четное")
    case var:
        print(var," -- много")
