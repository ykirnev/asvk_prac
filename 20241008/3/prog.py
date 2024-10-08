first_line = input()
a = input()
cnt_gas = 0
cnt_water = 0
wide = 2
height = len(a)
while a != first_line:
    wide += 1
    for i in range(len (a)):
        if a[i] == '.':
            cnt_gas += 1
        if a[i] == '~':
            cnt_water += 1
    a = input()
sm = cnt_water + cnt_gas
print('#' * wide)
wide = wide - 2
if cnt_water % wide != 0:
    cnt_water = (cnt_water // wide + 1) * wide
    cnt_gas = sm - cnt_water
for i in range(cnt_gas // wide):
    print('#' + '.' * wide + '#')
for i in range(cnt_water // wide):
    print('#' + '~' * wide + '#')
print('#' * (wide + 2))
total_width = 20
gas_ratio = cnt_gas / sm
water_ratio = cnt_water / sm
gas_width = round(gas_ratio * total_width)
water_width = round(water_ratio * total_width)
gas_line = '.' * gas_width
water_line = '~' * water_width
gas_fraction = f"{cnt_gas}/{sm}"
water_fraction = f"{cnt_water}/{sm}"
max_length = max(len(gas_line), len(water_line))
print(f"{gas_line:<{max_length}} {gas_fraction:>{len(gas_fraction) + 1}}")
print(f"{water_line:<{max_length}} {water_fraction:>{len(water_fraction) + 1}}")