from multiplier import multiplier
from fractions import Fraction
from decimal import Decimal

print(multiplier('1/6', '2/3', Fraction))
print(multiplier('0.1', '5.0', float))
print(multiplier('2.3', '4.5', Decimal))
