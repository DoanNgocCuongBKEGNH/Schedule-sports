from ortools.linear_solver import pywraplp
import itertools

def input(filename):
    with open(filename) as f:
        n, k = [int(x) for x in f.readline().split()]
        d = [[int(x) for x  in f.readline().split()] for i in range(n + 1)]
        for i in range(n+1):
            d[i].append(d[i][0])
        return n, k, d
    
n, k , d = input('data1.txt')

A = []
for i in range(n+1):
    for j in range(1, n+2):
        if i!= j and (i,j) != (0, n+1):
            A.append((i,j))
Ao = lambda x: (j for (i,j) in A if i == x)
Ai = lambda x: (j for (j,i) in A if i == x)

solver = pywraplp.Solver('MIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
INF = solver.infinity()

# Decision variables
x = [[[solver.IntVar(0, 1, f'x[{q}][{i}][{j}]') for j in range(n+2)] for i in range(n+1)] for q in range(k)]

z = solver.IntVar(0, INF, 'z')       
#Constraints
for q in range(k):
    c1 = solver.Constraint(1,1)
    for j in Ao(0):
        c1.SetCoefficient(x[q][0][j], 1)
        
    c2 = solver.Constraint(1,1)
    for i in Ai(n+1):
        c2.SetCoefficient(x[q][i][n+1], 1)
        
    cs = solver.Constraint(0, INF)
    cs.SetCoefficient(z, 1)
    for (i,j) in A:
        cs.SetCoefficient(x[q][i][j], - d[i][j])
        
for j in range(1, n+1):
    c6 = solver.Constraint(1,1)
    for q in range(k):
        for i in Ai(j):
            c6.SetCoefficient(x[q][i][j], 1)
                
for i in range(1, n+1):
    for q in range(k):
        c7 = solver.Constraint(0,0)
        for j in Ai(i):
            c7.SetCoefficient(x[q][j][i], 1)
        for l in Ao(i):
            c7.SetCoefficient(x[q][i][l], -1)
            
#SEC
def findsubsets(n,m):
    lst = [int(x) for x in range(n)]
    return set(itertools.combinations(lst,m))

for q in range(k):
    for length in range(2, n+1):
        subs = findsubsets(n+1, length)
        for u in subs:
            cstr = solver.Constraint(0, length-1)
            for (i,j) in A:
                if i in u and j in u:
                    cstr.SetCoefficient(x[q][i][j], 1)
'''                    
#Objective1
obj = solver.Objective()
obj.SetCoefficient(z, 1)
'''
#Objective2
obj = solver.Objective()
for q in range(k):
    for (i,j) in A:
        obj.SetCoefficient(x[q][i][j], d[i][j])
        
obj.SetMinimization()

rs = solver.Solve()

print(f'Optimal objective value = {obj.Value()}')  
def findNext(q,i):
    for j in Ao(i):
	    if x[q][i][j].solution_value() > 0:
		    return j
def route(q):
    s = '0 - '
    i = findNext(q,0)
    while i != n+1:
        s = s + str(i) + ' - '
        i = findNext(q,i)
    s = s + str(0)
    return s
    
for q in range(k):
    l = 0
    print('Route[' + str(q) +'] = '+ route(q))
    for i,j in A:
        if x[q][i][j].solution_value() > 0:
            l += d[i][j]
            if j != n+1:
	            print('(',i,'-',j,')')
            else:
                print('(',i,'-',0,')')	
    print('Length =', l)

        
    
        
    
    
