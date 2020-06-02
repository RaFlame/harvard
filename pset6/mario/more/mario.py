from cs50 import get_int

#Get user input
while True:
    n = get_int("Height: ")
    if n >= 0 and n <= 23:
        break
        
for i in range(n):
    print(' ' * (n-1-i), end="")
    print('#' * (i + 1), end="")
    print('  ', end= "")
    print('#' * (i + 1))