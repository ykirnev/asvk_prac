import math
import sys

def parse_number(val):
    try:
        return float(val)
    except ValueError:
        return 0.0
def interpret_assembler(program):
    lines = program.splitlines()
    coms = []
    labels = {}
    vars = {}
    for i, line in enumerate(lines):
        line = line.lstrip()
        if not line:
            continue
        if ":" in line:
            label, _, rest = line.partition(":")
            labels[label.strip()] = len(coms)
            line = rest.lstrip()
        if not line:
            continue
        parts = line.split()
        coms.append(parts)
    for com in coms:
        if com[0].startswith("if") and len(com) == 4:
            label = com[3]
            if label not in labels:
                return
    cnt = 0
    output = []
    while cnt < len(coms):
        com = coms[cnt]
        op = com[0]
        match op:
            case "stop":
                break
            case "store" if len(com) == 3:
                val = parse_number(com[1])
                vars[com[2]] = val
            case op if op in {"add", "sub", "mul", "div"} and len(com) == 4:
                src = vars.get(com[1], 0.0)
                operand = vars.get(com[2], 0.0)
                dest = com[3]
                match op:
                    case "add":
                        vars[dest] = src + operand
                    case "sub":
                        vars[dest] = src - operand
                    case "mul":
                        vars[dest] = src * operand
                    case "div":
                        vars[dest] = src / operand if operand != 0 else math.inf

            case op if op.startswith("if") and len(com) == 4:
                src = vars.get(com[1], 0.0)
                operand = vars.get(com[2], 0.0)
                label = com[3]
                match op:
                    case "ifeq" if src == operand:
                        cnt = labels[label]
                        continue
                    case "ifne" if src != operand:
                        cnt = labels[label]
                        continue
                    case "ifgt" if src > operand:
                        cnt = labels[label]
                        continue
                    case "ifge" if src >= operand:
                        cnt = labels[label]
                        continue
                    case "iflt" if src < operand:
                        cnt = labels[label]
                        continue
                    case "ifle" if src <= operand:
                        cnt = labels[label]
                        continue
            case "out" if len(com) == 2:
                val = vars.get(com[1], 0.0)
                output.append(val)
        cnt += 1
    for val in output:
        print(val)
s = sys.stdin.read()
interpret_assembler(s)