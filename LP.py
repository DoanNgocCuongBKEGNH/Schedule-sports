# pip install ortools
from ortools.linear_solver import pywraplp

solver = pywraplp.CreateSolver('DEMO', 'CHC')
INF = solve.infinity()

c1 = solver.Constraint(4, 4)
c1.SetCoefficient(x[1], 1)
c1.SetCoefficient(x[2], 1)
c1.SetCoefficient(x[3], -1)
c1.SetCoefficient(x[4], -1)
c1.SetCoefficient(x[5], 1)
c1.SetCoefficient(x[6], 0)
c1.SetCoefficient(x[7], 0)

c2 = solver.Constraint(7, 7)
c2.SetCoefficient(x[1], 1)
c2.SetCoefficient(x[2], 0)
c2.SetCoefficient(x[3], 1)
c2.SetCoefficient(x[4], 1)
c2.SetCoefficient(x[5], 0)
c2.SetCoefficient(x[6], 1)
c2.SetCoefficient(x[7], 0)

c3 = solver.Constraint(2, 2)
c3.SetCoefficient(x[1], 1)
c3.SetCoefficient(x[2], -1)
c3.SetCoefficient(x[3], -1)
c3.SetCoefficient(x[4], 0)
c3.SetCoefficient(x[5], 0)
c3.SetCoefficient(x[6], 0)
c3.SetCoefficient(x[7], 1)

obj = solver.Objective()
obj.SetCoefficient(x[1], 0)
obj.SetCoefficient(x[2], 0)
obj.SetCoefficient(x[3], 0)
obj.SetCoefficient(x[4], 0)
obj.SetCoefficient(x[5], -1)
obj.SetCoefficient(x[6], -1)
obj.SetCoefficient(x[7], -1)

res_status = solver.Solve()

if res_status != pywraplp.solver.OPTIMAL: 
    print('can not')
else: 
    print(solver.Objective().Value())

print('x1 =', x1.solution_value())