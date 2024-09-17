a, b, c = eval(input())
if (a > 0 and b > 0 and c > 0): 
    if (a < b + c and b < a + c and c < a + b):
        print("Yes")
        exit(0)
print("No")
        
