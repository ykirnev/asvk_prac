def difference(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a - b
    else:
        res = [x for x in a if x not in b]
        if isinstance(a, tuple):
            return tuple(res)
        else:
            return res

x = input()
left_pos = x.find('(') if '(' in x else x.find('[')
if left_pos == -1:
    a, b = x.split(',', 1)
else:
    depth = 0
    for i, char in enumerate(x):
        if char in '([':
            depth += 1
        elif char in ')]':
            depth -= 1
        elif char == ',' and depth == 0:
            a = x[:i]
            b = x[i+1:].strip()
            break
a = eval(a)
b = eval(b)
res = difference(a, b)
print(res)

