def difference(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a - b
    else:
        res = [x for x in a if x not in b]
        if isinstance(a, tuple):
            return tuple(res)
        else:
            return res
