# Input #
'''
4
0 1 2 3
1 0 4 5
2 4 0 6
3 5 6 0
'''
import sys
def input(): 
    [n] = [int(x) for x in sys.stdin.readline().split()]
    E = []
    for i in range(n): 
        row = [int(x) for x in sys.stdin.readline().split()]
        E.append(row)
    print(n)
    print(E)

# file object = open(file_name [, access_mode][, buffering])

input()