import decimal
from decimal import Decimal as dec
def esum(N, one):
    sum = 0
    fact = 1
    for i in range(1, N):
        sum += one / fact
        fact *= i
    return sum

decimal.getcontext().prec = 100
print(esum(100, dec(1)))