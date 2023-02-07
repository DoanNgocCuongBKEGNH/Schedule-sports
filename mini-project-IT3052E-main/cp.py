from ortools.sat.python import cp_model
import itertools

def input(filename):
    with open(filename) as f:
        n, k = [int(x) for x in f.readline().split()]
        d = [[int(x) for x  in f.readline().split()] for i in range(n + 1)]
        for i in range(n+1):
            d[i].append(d[i][0])
        return n, k, d

n, k , d = input('data1.txt')
M = 0
for i in range(len(d)):
    M += sum(d[i])

A = []
for i in range(n+1):
    for j in range(1, n+2):
        if i!= j and (i,j) != (0, n+1):
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
        K = [[] for q in range(k)]
        for q in range(k):
            for (i,j) in A:
                if self.Value(self.__variables[q][i][j]) > 0:
                    print(q,i,j)
                    K[q].append((i,j))
        for q in range(k):
            i = 0
            route = '0->'
            while True:
                #print(i)
                i = Findnext(K[q], i)
                if i!= n+1:
                    route += str(i)
                    route += '->'
                else:
                    route += str(0)
                    break
            s = sum([d[i][j] for (i,j) in K[q]])
            print(f'Route[{q}]: {route}, length: {s}' )
    def solution_count():
        return self.__solution_count

model = cp_model.CpModel()
#Variables
x = [[[model.NewIntVar(0,1, f'x[{q}][{i}][{j}]') for j in range(n+2)] for i in range(n+1)] for q in range(k)]
z = model.NewIntVar(0, M, 'z')
#Constraints
for q in range(k):
    model.Add(sum(x[q][0][j] for j in Ao(0)) == 1)
    model.Add(sum(x[q][i][n+1] for i in Ai(n+1)) == 1)
    model.Add(sum(x[q][i][j]*d[i][j] for (i,j) in A) <= z)

for i in range(1, n+1):
    model.Add(sum(x[q][i][j] for j in Ao(i) for q in range(k)) == 1)

for i in range(1, n+1):
    for q in range(k):
        model.Add(sum(x[q][j][i] for j in Ai(i)) == sum(x[q][i][l] for l in Ao(i)))

#SEC
def findsubsets(n,m):
    lst = [int(x) for x in range(n)]
    return set(itertools.combinations(lst,m))
for q in range(k):
    for length in range(2, n+1):
        subs = findsubsets(n+1, length)
        for u in subs:
            B = [(i,j) for (i,j) in A if (i in u and j in u)]
            model.Add(sum(x[q][i][j] for (i,j) in B) <= length-1)
'''
#Objective 1            
model.Minimize(z)
'''
#Objective 2
model.Minimize(sum(x[q][i][j] * d[i][j] for (i,j) in A for q in range(k)))

solver = cp_model.CpSolver()
vars = [x[q][i][j] for q in range(k) for (i,j) in A]
solution_printer = VarArraySolutionPrinter(vars)

status = solver.Solve(model, solution_printer)
#print(solver.ResponseStats())
if status == cp_model.OPTIMAL:
        print('Optimal value = %i' % solver.ObjectiveValue())
