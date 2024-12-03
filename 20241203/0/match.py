t = "qwre ASDF"
match t.split():
    case []:
        print("empty")
    case ["qwe"]:
        print("No doubt")
    case [str(x)]:
        print('List of 1 str')
    case [x]:
        print("Size 1")
    case[_, *tail]:
        print("List with tail", tail)
