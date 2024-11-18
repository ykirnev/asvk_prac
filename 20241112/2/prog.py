def triangleSquare(input_str):
    try:
        a = eval(input_str)
        if not (
            isinstance(a, tuple) and
            len(a) == 3 and
            all(isinstance(point, tuple) and len(point) == 2 for point in a)
        ):
            raise ValueError
        (x1, y1), (x2, y2), (x3, y3) = a
        if not all(isinstance(coord, (int, float)) for coord in [x1, y1, x2, y2, x3, y3]):
            raise ValueError
        if (x2 - x1) * (y3 - y1) == (x3 - x1) * (y2 - y1):
            raise ArithmeticError

        area = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2)
        return round(area, 2)

    except (SyntaxError, NameError, TypeError, ValueError):
        return "Invalid input"
    except ArithmeticError:
        return "Not a triangle"

while True:
    input_str = input()
    result = triangleSquare(input_str)
    if result == "Invalid input":
        print(result)
    elif result == "Not a triangle":
        print(result)
    else:
        print(result)
        break

