def Pareto(pairs):
    answer = []
    for i in pairs:
        flag = 1
        for j in pairs:
            if i[0] <= j[0] and i[1] <= j[1] and (i[0] < j[0] or i[1] < j[1]):
                flag = 0
                break
        if flag == 1:
            answer.append(i)
    return answer
print(tuple(Pareto(eval(input()))))