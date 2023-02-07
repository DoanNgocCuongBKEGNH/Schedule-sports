# import sys
# '''
# input mảng 1 chiều. Input 1 2 3 4 -> [1, 2, 3, 4]
# arr = list(map(int, input().split()))
# arr = [int(x) for x in input().split()]
# '''

# def input(): 
#     [n] = [int(x) for x in sys.stdin.readline().split()]
#     c = []
#     for i in range(n): 
#         row = [int(x) for x in sys.stdin.readline().split()]
#         c.append(row)
#     return n, c
# n, c = input()
# print(c)

# x = [0 for i in range(n)]
# x_best = [0 for i in range(n)]
# f_best = 100000 #reprents the best objective value
# f = 0 # reprếnts the total travel cost (distance)
# mark = [False for v in range(n)]

# def solution(): 
#     """check if the current solution is better than
#      best solution found so far if so, then update..."""
#     global f_best        # Global Variables >< Local Variables
#     # UnboundLocalError: local variable 'f_best' referenced before assignment
#     if f + c[x[n - 1]] [x[0]] < f_best: 
#         f_best = f + c[x[n - 1]] [x[0]]
#         x_best[:] = x[:]
#         print('current solution', x, '-> update', f_best)


# def Try(k): 
#     global f # Để dùng được f variable đã khai báo ở trên ở trong def Try(k)
#     # UnboundLocalError: local variable 'f' referenced before assignment
#     for v in range(n): 
#         if mark[v] == False: #value v has not been used
#             x[k] = v
#             f = f + c [x[k - 1]] [x[k]]
#             mark [v] = True # mark value v as it is used
#             if k == n - 1: 
#                 solution()
#             else: 
#                 # Try(k + 1)
#                 # Thêm 2 dòng này trước dòng Try(k + 1) -> Thuật toán tối ưu hơn. 
#                 g = f + cm * (n - k)
#                 if g < f_best: Try(k + 1)
                
#             mark [v] = False
#             f = f - c[x[k - 1]] [x[k]]

# # Khởi tạo cm = min c[i][j]
# cm = 100000 
# for i in range(n): 
#     for j in range(n): 
#         if i != j and cm > c[i][j]: 
#             cm = c[i][j]

# x[0] = 0
# mark[0] = True
# Try(1)

'''
Input BCA problem


'''
# class SubSetGenerator: 
#     def _init__(self, N): 
#         self.N = N
#         self.x = [0 for i in range(N + 1)] 

#     def __CollectSubset__(self): 
#         S = []
#         for i in range(1, N + 1): 
#             if self.x[i] == 1: 
#                 S.append(i)
#         return S

#     def GenerateFirstSubset(self): 
#         return self.__CollectSubset__()

#     def GenerateNextSubset(self): 
#         'Sinh tap con'
#         N = self.N
#         x = self.x 
#         i = N
#         while i >= 1 and x[i] == 1: 
#             i = i - 1
#         if i == 0: 
#             return None 

#         x[i] = 1
#         for j in range(i + 1, N+1): 
#             x[j] = 0
#         return self.__CollectSubset__()

# SG = SubSetGenerator(4)
# S = SG.GenerateFirstSubset()
# while True: 
#     print(S)
#     S = SG.GenerateNextSubset()
#     if S == None: 
#         break   
# # tren nay la thuat toan sinh cac tap con 
from ortools.linear_solver import pywraplp
import sys

class SubSetGenerator: 
    def __init__(self, N): # thieu 1 dau gach o init
        self.N = N
        self.x = [0 for i in range(N + 1)] 

    def __CollectSubset__(self): 
        S = []
        for i in range(1, self.N + 1): 
            if self.x[i] == 1: 
                S.append(i)
        return S

    def GenerateFirstSubset(self): 
        return self.__CollectSubset__()

    def GenerateNextSubset(self): 
        'Sinh tap con'
        N = self.N
        x = self.x 
        i = N
        while i >= 1 and x[i] == 1: 
            i = i - 1
        if i == 0: 
            return None 

        x[i] = 1
        for j in range(i + 1, N+1): 
            x[j] = 0
        return self.__CollectSubset__()

def input(): 
    [n] = [int(x) for x in sys.stdin.readline().split()]
    d = []
    d.append(([]))
    for i in range(n): 
        row = [int(x) for x in sys.stdin.readline().split()]
        row.insert(0, 0)
        d.append(row)
    return n, d


 
# tren nay la thuat toan sinh cac tap con 

N, d = input()

# solver = pywraplp.Solver.CreateSolver('TSP','CBC')
solver = pywraplp.Solver.CreateSolver('CBC')
X = [[solver.IntVar(0, 1, 'X' + str(i) + ',' + str(j) + ')') for j in range(N + 1)] for i in range(N + 1)]

for i in range(1, N + 1): 
    c = solver.Constraint(1, 1)
    for j in range(1, N + 1): 
        if i != j: 

            c.SetCoefficient(X[j][i], 1)
    
    c = solver.Constraint(1, 1)    
    for j in range(1, N + 1): 
        c.SetCoefficient(X[i][j], 1)

# state SEC Sub-Tour Elimnation Constraint
SG = SubSetGenerator(N)
S = SG.GenerateFirstSubset()
while True: 
    # print(S) # print cac tap con cua
    if len(S) >= 2 and len(S) < N: 
        c = solver.Constraint(0, len(S) - 1)
        for i in S: 
            for j in S: 
                if i != j: 
                    c.SetCoefficient(X[i][j], 1)
    S = SG.GenerateNextSubset()
    if S == None: 
        break  

# objective function
objective = solver.Objective()
for i in range (1, N + 1): 
    for j in range(1, N + 1): 
        if i != j: 
            objective.SetCoefficient(X[i][j], d[i][j])
# solver.SetMinimization()
result_status = solver.Solve()
if result_status != pywraplp.Solver.OPTIMAL: 
    print('cannot find optimal solution')
else: 
    print('optimal obj value =', solver.Objective().Value())

for i in range(1, N + 1): 
    for j in range(1, N + 1): 
        if X[i][j].solution_value() > 0: 
            print('(', i, ',', j, ')')

'''
optimal obj value = 7.0
( 1 , 2 )
( 2 , 4 )
( 3 , 1 )
( 4 , 3 )
'''

# print soulution 
def findNext(current): 
    for i in range(1, N  + 1): 
        if X[current][i].solution_value() > 0: 
            return i 
    return -1 # NOT FOUND 

def extractSolutionRoute(): 
    route = []
    current = 1
    route.append(1)
    for i in range(2, N + 1): 
        nextPoint = findNext(current)
        route.append(nextPoint)
        current = nextPoint
    return route

print(N)
route = extractSolutionRoute() # -> print(route) : [1, 2, 4, 3]
for i in route: 
    print(i, end = ' ')
'''
Test case: TSP - 10
10
0 2 2 7 5 7 4 10 8 9 
6 0 2 2 4 5 3 7 2 4 
4 2 0 1 5 8 2 9 3 1 
9 3 3 0 8 5 6 1 3 2 
7 2 1 2 0 5 8 9 5 1 
1 2 5 9 9 0 6 2 2 4 
3 7 2 4 1 6 0 6 6 6 
4 5 7 8 7 4 6 0 7 7 
6 1 2 8 1 7 9 9 0 9 
8 9 4 6 2 8 9 10 6 0 
'''
