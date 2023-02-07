import time
before = time.time()

from ortools.sat.python import cp_model
import copy
import time

class VarArrayAndObjectiveSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions (objective, variable values, time)."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__start_time = time.time()

    def on_solution_callback(self):
        """Called on each new solution."""
        current_time = time.time()
        obj = self.ObjectiveValue()
        print('Solution %i, time = %0.2f s, objective = %i' %
              (self.__solution_count, current_time - self.__start_time, obj))
        for i in range(len(self.__variables)):
            for j in range(len(self.__variables)):
                print(self.Value(self.__variables[i][j]), end = ' ')
            print()
        print()
        self.__solution_count += 1

    def solution_count(self):
        """Returns the number of solutions found."""
        return self.__solution_count
def OR_Tools_solve(input):
    
    distance_matrix = input
    N = len(input)

    model = cp_model.CpModel()

    x = []
    for i in range(N):
        row = [None]*N
        row[i] = 0
        x.append(row)

    for i in range(N):
        for j in range(N):
            if i == j:
                x[i][i] = model.NewIntVar(0,0,'x[%i][%i]' % (i,i))
            else:
                x[i][j] = model.NewIntVar(0,2*N - 2, 'x[%i][%i]' %(i,j))

    for i in range(N):
        c = list(x[j][i] for j in range(N))
        c.pop(i)
        cnr = x[i] + c
        model.AddAllDifferent(cnr)
    
    y = []
    for i in range(N):
        y_row = []
        for j in range(2*N - 1):
            row = [None]*(2*N - 1)
            row[i] = 0
            y_row.append(row)
        y.append(y_row)
    for i in range(N):
        for j in range(2*N - 1):
            for k in range(2*N - 1):
                y[i][j][k] = model.NewBoolVar('y[%i][%i][%i]' % (i,j,k))


    obj_func = 0

    for team in range(N):

        indexes = list((team,j) for j in range(0,N) if team!= j) + list((j,team) for j in range(0,N) if team!= j)
        index_0 = (team,team)

        for i in range(len(indexes)):
            model.Add(x[indexes[i][0]][indexes[i][1]] == x[index_0[0]][index_0[1]] + 1).OnlyEnforceIf(y[team][0][i + 1])
            model.Add(x[indexes[i][0]][indexes[i][1]] != x[index_0[0]][index_0[1]] + 1).OnlyEnforceIf(y[team][0][i + 1].Not())
        for i in range(len(indexes)):
            indexes_copy = copy.deepcopy(indexes)
            for j in range(len(indexes_copy)):
                if i != j:
                    model.Add(x[indexes[i][0]][indexes[i][1]] == x[indexes_copy[j][0]][indexes_copy[j][1]] - 1).OnlyEnforceIf(y[team][i + 1][j + 1])
                    model.Add(x[indexes[i][0]][indexes[i][1]] != x[indexes_copy[j][0]][indexes_copy[j][1]] - 1).OnlyEnforceIf(y[team][i + 1][j + 1].Not())
        
        others = list(i for i in range(N) if i!= team)
        for i in range(2*N - 1):
            for j in range(2*N - 1):
                if i == 0:
                    if j == 0:
                        obj_func += 0
                    elif j <= N-1:
                        obj_func += distance_matrix[team][others[j - 1]] * y[team][0][j]
                    else:
                        obj_func += distance_matrix[team][team] * y[team][0][j]
                elif i <= N-1:
                    if j == 0:
                        obj_func += 0
                    elif j <= N-1:
                        obj_func += distance_matrix[others[i - 1]][others[j - 1]] * y[team][i][j]
                    else:
                        obj_func += distance_matrix[others[i - 1]][team] * y[team][i][j]
                else:
                    if j == 0:
                        obj_func += 0
                    elif j <= N-1:
                        obj_func += distance_matrix[team][others[j - 1]] * y[team][i][j]
                    else:
                        obj_func += distance_matrix[team][team] * y[team][i][j]

    model.Minimize(obj_func)
    
    solver = cp_model.CpSolver()
    solution_printer = VarArrayAndObjectiveSolutionPrinter(x)
    status = solver.Solve(model, solution_printer)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f'Minimum of objective function: {solver.ObjectiveValue()}\n')
        # print(solver.Value())
        # TypeError: CpSolver.Value() missing 1 required positional argument: 'expression'
        for i in range(N):
            for j in range(N):
                print(solver.Value(x[i][j]), end = ' ')
            print()
    

    else:
        print('No solution found.')
    
    print('\nStatistic')
    print(f'  status : {solver.StatusName(status)}')
    print(f'  conflicts: {solver.NumConflicts()}')
    print(f'  branches : {solver.NumBranches()}')
    print(f'  wall time: {solver.WallTime()} s')
    print(f'  Reasonable cost using OR-Tools: {solver.ObjectiveValue()}')

distance_matrix = [[0, 1, 2, 3], [1, 0, 4, 5], [2, 4, 0, 6], [3, 5, 6, 0]]
print('When using Or - Tool:')
OR_Tools_solve(distance_matrix)


runtime = time.time() - before
print(f'Runtime: {runtime}')