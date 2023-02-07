import sys
from ortools.linear_solver import pywraplp

def input():
    [N] = [int(x) for x in sys.stdin.readline().split()]
    d = []
    d.append([])
    for i in range(N):
        r = [int(x) for x in sys.stdin.readline().split()]
        r.insert(0,0)
        d.append(r)
    return N, d

def CreateVariable(solver):
    # SECs: the set of sub-tours
    X = [[solver.IntVar(0,1,'X' + str(i) + ',' + str(j)+')') for j in range(N+1)] for i in range(N+1)]
    return X

# solver = pywraplp.Solver.CreateSolver('CBC')

def TSP_SEC(SECs):
    solver = pywraplp.Solver.CreateSolver('CBC')
    X = CreateVariable(solver)
    for i in range(1,N+1):
        c = solver.Constraint(1,1)
        for j in range(1,N+1):
            if i != j:
                c.SetCoefficient(X[i][j],1)
        c = solver.Constraint(1,1)
        for j in range(1,N+1):
            if j != i:
                c.SetCoefficient(X[j][i],1)
        
    for S in SECs:
        c = solver.Constraint(0,len(S)-1)
        for i in S:
            for j in S:
                if i!=j:
                    c.SetCoefficient(X[i][j],1)
    
    obj = solver.Objective()
    for i in range(1,N+1):
        for j in range(1,N+1):
            obj.SetCoefficient(X[i][j],d[i][j])
        
    res_stat = solver.Solve()
    if res_stat != pywraplp.Solver.OPTIMAL:
        print('cannot find optimal for sub-problem')
        return None
    else:
        print('optimal value sub-problem = ', solver.Objective().Value())
    
    s = [[X[i][j].solution_value() for i in range(N+1)] for j in range(N+1)]
    return s

def findnext(solution,current,cand):
    for i in cand:
        if solution[current][i] > 0:
            return i
    return -1 # not found

# def extractSolutionRoute(X,current):
#     route = []
#     route.append(current)
#     return route

def getfirst(S):
    for i in S:
        return i

def ExtractSubTour(solution):
    S = []
    # visited = [False for i in range(1,N+1)]
    cand = set()
    for i in range(1,N+1):
        cand.add(i)
    while len(cand)> 0:
        cur = getfirst(cand)
        T = set()
        T.add(cur)
        cand.remove(cur)
        while True:
            next = findnext(solution,cur,cand)
            if next == -1 :
                break
            T.add(next)
            cand.remove(next)
            cur = next
        if len(T) == N:
            return None
        S.append(T)
    if len(S) == 0:
        return None
    return S

def TSP():
    # solver = pywraplp.Solver.CreateSolver('CBC')
    SECs = []
    while True:
        solution = TSP_SEC(SECs)
        # S = ExtractSubTour(X)
        if solution == None:
            print('not feasible')
            break
        print('Found X')

        S = ExtractSubTour(solution)
        print(S)
        if S == None:
            print('found optimal solution')
            break
        for S1 in S:
            SECs.append(S1)

N,d = input()
TSP()
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