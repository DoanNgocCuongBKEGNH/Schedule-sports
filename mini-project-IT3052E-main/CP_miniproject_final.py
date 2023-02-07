from ortools.sat.python import cp_model
import itertools
import time

def input(filename):
    with open(filename) as f:
        N, K = [int(x) for x in f.readline().split()]
        d = [[int(x) for x  in f.readline().split()] for i in range(N + 1)]
        for i in range(N+1):
            d[i].append(d[i][0])
        return N, K, d
    
N, K , d = input('data.txt')
start_time=time.time()
M = 0
for i in range(len(d)):
    M += sum(d[i])

A = []
for i in range(N+1):
    for j in range(1, N+2):
        if i!= j and (i,j) != (0, N+1):
            A.append((i,j))
Ao = lambda x: (j for (i,j) in A if i == x)
Ai = lambda x: (j for (j,i) in A if i == x)

class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    #print intermediate solution
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
    def on_solution_callback(self):
        def Findnext(Kq, i):
            for u in Kq:
                if u[0] == i:
                    return u[1]        
        self.__solution_count += 1
        L = [[] for k in range(K)]
        for k in range(K):
            for (i,j) in A:
                if self.Value(self.__variables[k][i][j]) > 0:
                    L[k].append((i,j))
        for k in range(K):
            i = 0
            route = '0->'
            while True:
                #print(i)
                i = Findnext(L[k], i)
                if i!= N+1:
                    route += str(i)
                    route += '->'
                else:
                    route += str(0)
                    break
            s = sum([d[i][j] for (i,j) in L[k]])
            print(f'Route[{k}]: {route}, length: {s}' )
        #print()
    def solution_count():
        return self.__solution_count
    
model = cp_model.CpModel()
#Variables
x = [[[model.NewIntVar(0,1, f'x[{k}][{i}][{j}]') for j in range(N+2)] 
    for i in range(N+1)] for k in range(K)]
z = model.NewIntVar(0, M, 'z')
#Constraints
def basic_constraint():
    for k in range(K):
        model.Add(sum(x[k][0][j] for j in Ao(0)) == 1)
        model.Add(sum(x[k][j][N+1] for j in Ai(N+1)) == 1)
        
    
    for i in range(1, N+1):
        model.Add(sum(x[k][i][j] for j in Ao(i) for k in range(K)) == 1)
        model.Add(sum(x[k][j][i] for j in Ai(i) for k in range(K)) == 1)
    
    for i in range(1, N+1):
        for k in range(K):
            model.Add(sum(x[k][j][i] for j in Ai(i)) == sum(x[k][i][j] for j in Ao(i)))

#SEC
def findsubsets(N,m):
    lst = [int(x) for x in range(N)]
    return set(itertools.combinations(lst,m))
for k in range(K):
    for length in range(2, N+1):
        subs = findsubsets(N+1, length)
        for u in subs:
            B = [(i,j) for (i,j) in A if (i in u and j in u)]
            model.Add(sum(x[k][i][j] for (i,j) in B) <= length-1)

def first_obj():
    basic_constraint()
    for k in range(K):
        model.Add(sum(x[k][i][j]*d[i][j] for (i,j) in A) <= z)
    model.Minimize(z)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL:
       return solver.ObjectiveValue()
def second_obj():
    basic_constraint()
    result1= first_obj()   
    print(result1)
    for k in range(K):
        model.Add(sum(x[k][i][j]*d[i][j] for (i,j) in A) <= int(result1) )
        
    solver2 = cp_model.CpSolver()
    model.Minimize(sum(x[k][i][j] * d[i][j] for (i,j) in A for k in range(K)))
    solution_printer = VarArraySolutionPrinter(x)

    status = solver2.Solve(model, solution_printer)
    #print(solver.ResponseStats())
    if status == cp_model.OPTIMAL:
        print('Optimal value = %i' % solver2.ObjectiveValue())
second_obj() 
end_time=time.time()
print('time: ', end_time-start_time)
