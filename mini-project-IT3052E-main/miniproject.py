from os import name, replace
from ortools.linear_solver import pywraplp
import itertools

def input(filename):
    with open(filename) as f:
        n,k = [int(x) for x in f.readline().split()]
        d=[]
        for i in range(n+1):
            li = [int(x) for x in f.readline().split()]
            li.append(li[0])
            d.append(li)
    return n,k,d
N,K,d=input('input.txt')

A = []

for i in range(N+2):
    for j in range(N+2):
        if i!=j and j!=0 and i!=N+1:
            A.append([i,j])
Ao = lambda x: (j for i, j in A if i == x)
Ai = lambda x: (i for i, j in A if j == x)

solver = pywraplp.Solver('CVRP_MIP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
INF = solver.infinity()
# Decision variables
x = [[[solver.IntVar(0, 1, f'x[{k}][{i}][{j}]') for j in range(N+2)] for i in range(N+2)] for k in range(K)]
z = solver.IntVar(0,10000, 'z')

def findsubsets(n,m): #this function will be used in the subtour-eliminating constraint
    n=[int(x) for x in range(n)]
    lst= set(itertools.combinations(n, m))
    return lst

def basic_constraint():#these constraints can be used for both function
    for i in range(1,N+1):
        constraint=solver.Constraint(1,1)
        for k in range(K):
            for j in range(1,N+1):
                constraint.SetCoefficient(x[k][j][i],1)

    for i in range(1,N+1): 
        constraint=solver.Constraint(1,1)
        for k in range(K):
            for j in Ao(i):
                constraint.SetCoefficient(x[k][i][j],1)

    for i in range(1,N+1):
        constraint=solver.Constraint(1,1)
        for k in range(K):
            for j in Ai(i):
                constraint.SetCoefficient(x[k][j][i],1)

    for i in range(1,N+1):#the person get in i = the person out of i
        for k in range(K):
            constraint=solver.Constraint(0,0)
            for j in Ai(i):
                constraint.SetCoefficient(x[k][j][i],1)
            for j in Ao(i):
                constraint.SetCoefficient(x[k][i][j],-1)

    for k in range(K):
        constraint=solver.Constraint(1,1)
        for j in range(1,N+1):
            constraint.SetCoefficient(x[k][0][j],1)

    for k in range(K):
        constraint=solver.Constraint(1,1)
        for j in range(1,N+1):
            constraint.SetCoefficient(x[k][j][N+1],1)
#eliminate_subtour

    for k in range(K):
        for l in range(2,N+1):
            subs=findsubsets(N+1,l)
            for t in subs:
                constraint=solver.Constraint(0,l-1)
                for i in t:
                    for j in t:
                        constraint.SetCoefficient(x[k][i][j],1)
def first_obj():
    basic_constraint()
    #this constraint below is only for objective 1
    for k in range(K): 
        constraint=solver.Constraint(0,INF) 
        constraint.SetCoefficient(z,1)  
        for i,j in A:
            constraint.SetCoefficient(x[k][i][j],-d[i][j])
    #First objective   
    obj1=solver.Objective()
    obj1.SetCoefficient(z,1)
    obj1.SetMinimization()

    rs1=solver.Solve()
    return (obj1.Value())

def second_obj():
    basic_constraint()
    result1= first_obj()
#Constraint for objective 2 such that objective 1 must be satisfied
    for k in range(K):
        constraint2=solver.Constraint(0,result1+1)
        for i,j in A:
            constraint2.SetCoefficient(x[k][i][j],d[i][j])
#Second objective    
    obj2=solver.Objective()
    for k in range(K):
        for i,j in A:
            obj2.SetCoefficient(x[k][i][j],d[i][j])
    obj2.SetMinimization()
    rs2=solver.Solve()
    result2=obj2.Value()
    #print the result
    print('Optimal objective value =',result2-result1)
    for k in range(K):
        route,path=[],[0]
        for i,j in A:
            if x[k][i][j].solution_value() > 0:
                route.append([i,j])
        temp=0
        while len(path)<len(route)+1:
            for y in route:
                if y[0]==temp:
                    temp=y[1]
                    path.append(temp)
        remake_path=[0 if x==N+1 else x for x in path]           
        print(k,':', '->'.join(str(x) for x in remake_path))
second_obj()



    



