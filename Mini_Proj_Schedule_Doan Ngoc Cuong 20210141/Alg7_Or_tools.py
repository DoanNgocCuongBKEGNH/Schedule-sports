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
        # for i in range(N):
        #     for j in range(N):
        #         print(solver.Value(x[i][j]), end = ' ')
        #     print()
    

    else:
        print('No solution found.')
    
    print('\nStatistic')
    print(f'  status : {solver.StatusName(status)}')
    print(f'  conflicts: {solver.NumConflicts()}')
    print(f'  branches : {solver.NumBranches()}')
    print(f'  wall time: {solver.WallTime()} s')
    print(f'  Reasonable cost using OR-Tools: {solver.ObjectiveValue()}')

distance_matrix = [[0, 1, 2, 3], [1, 0, 4, 5], [2, 4, 0, 6], [3, 5, 6, 0]]
distance_matrix = [[0, 9, 4, 7, 9, 7], [9, 0, 2, 1, 4, 8], [4, 2, 0, 5, 7, 2], [7, 1, 5, 0, 9, 3], [9, 4, 7, 9, 0, 6], [7, 8, 2, 3, 6, 0]]
distance_matrix = [[0, 9, 3, 9, 8, 5, 3, 1, 4, 1], [9, 0, 4, 6, 8, 4, 9, 7, 8, 8], [3, 4, 0, 3, 1, 2, 5, 5, 3, 9], [9, 6, 3, 0, 7, 9, 6, 1, 7, 1], [8, 8, 1, 7, 0, 7, 6, 3, 5, 7], [5, 4, 2, 9, 7, 0, 1, 4, 8, 5], [3, 9, 5, 6, 6, 1, 
0, 1, 8, 2], [1, 7, 5, 1, 3, 4, 1, 0, 9, 7], [4, 8, 3, 7, 5, 8, 8, 9, 0, 8], [1, 8, 9, 1, 7, 5, 2, 7, 8, 0]]

# n = 32 
distance_matrix = [[0, 8, 8, 8, 1, 8, 4, 1, 6, 3, 4, 9, 8, 7, 7, 5, 9, 8, 4, 3, 9, 1, 3, 7, 5, 4, 4, 6, 3, 4, 4, 7], [8, 0, 
3, 8, 7, 2, 9, 4, 9, 6, 3, 7, 1, 4, 8, 4, 3, 8, 8, 1, 9, 7, 6, 6, 2, 3, 6, 1, 8, 7, 6, 8], [8, 3, 0, 3, 8, 7, 4, 5, 5, 8, 3, 7, 1, 3, 9, 8, 8, 7, 4, 5, 8, 2, 1, 3, 3, 2, 4, 6, 8, 6, 8, 2], [8, 8, 3, 0, 8, 5, 8, 9, 8, 4, 7, 3, 6, 7, 3, 7, 5, 9, 7, 2, 5, 7, 5, 6, 5, 9, 3, 3, 1, 1, 8, 7], [1, 7, 8, 8, 0, 9, 3, 7, 3, 9, 
6, 6, 2, 6, 1, 6, 7, 5, 1, 8, 3, 7, 5, 4, 2, 3, 6, 5, 5, 6, 6, 1], [8, 2, 7, 5, 9, 0, 9, 5, 2, 1, 6, 4, 2, 3, 6, 8, 7, 2, 7, 4, 2, 7, 6, 9, 6, 5, 8, 2, 6, 7, 3, 1], [4, 9, 4, 8, 3, 9, 0, 2, 5, 9, 1, 3, 1, 5, 5, 7, 6, 8, 1, 6, 4, 6, 4, 6, 4, 8, 7, 1, 1, 8, 7, 7], [1, 4, 5, 9, 7, 5, 2, 0, 2, 3, 3, 3, 9, 9, 3, 4, 6, 7, 
1, 7, 4, 5, 1, 6, 7, 8, 4, 8, 2, 9, 9, 2], [6, 9, 5, 8, 3, 2, 5, 2, 0, 6, 3, 1, 4, 4, 8, 1, 5, 5, 1, 8, 9, 3, 8, 2, 8, 4, 4, 2, 1, 2, 1, 2], [3, 6, 8, 4, 9, 1, 9, 3, 6, 0, 3, 3, 6, 1, 7, 3, 1, 8, 1, 3, 2, 6, 6, 4, 5, 1, 9, 5, 3, 8, 7, 5], [4, 3, 3, 7, 6, 6, 1, 3, 3, 3, 0, 6, 9, 8, 6, 7, 5, 1, 9, 6, 9, 5, 4, 8, 7, 9, 
3, 6, 2, 8, 3, 4], [9, 7, 7, 3, 6, 4, 3, 3, 1, 3, 6, 0, 2, 5, 6, 9, 3, 6, 9, 8, 5, 2, 1, 6, 2, 4, 9, 5, 1, 6, 3, 4], [8, 1, 1, 6, 2, 2, 1, 9, 4, 6, 9, 2, 0, 5, 6, 8, 5, 1, 3, 4, 8, 6, 8, 9, 8, 6, 6, 1, 8, 3, 7, 5], [7, 4, 3, 7, 6, 3, 5, 9, 4, 1, 8, 5, 5, 0, 2, 2, 5, 4, 9, 1, 8, 3, 2, 8, 3, 6, 6, 5, 7, 1, 8, 4], [7, 8, 9, 3, 1, 6, 5, 3, 8, 7, 6, 6, 6, 2, 0, 5, 6, 9, 5, 6, 8, 1, 4, 8, 5, 2, 8, 8, 2, 2, 5, 8], [5, 4, 8, 7, 
6, 8, 7, 4, 1, 3, 7, 9, 8, 2, 5, 0, 2, 6, 5, 3, 3, 6, 5, 5, 8, 9, 6, 8, 5, 6, 4, 8], [9, 3, 8, 5, 7, 7, 6, 6, 5, 1, 5, 3, 5, 5, 6, 2, 0, 1, 3, 7, 1, 1, 6, 4, 3, 2, 6, 8, 6, 7, 8, 8], [8, 8, 7, 9, 5, 2, 8, 7, 5, 8, 1, 6, 1, 4, 9, 6, 1, 0, 6, 9, 5, 6, 6, 5, 2, 5, 4, 3, 3, 4, 3, 8], [4, 8, 4, 7, 1, 7, 1, 1, 1, 1, 9, 9, 
3, 9, 5, 5, 3, 6, 0, 2, 6, 1, 5, 4, 5, 3, 3, 3, 8, 1, 5, 9], [3, 1, 5, 2, 8, 4, 6, 7, 8, 3, 6, 8, 4, 1, 6, 3, 7, 9, 2, 0, 9, 9, 6, 7, 6, 9, 9, 2, 2, 8, 3, 6], [9, 9, 8, 5, 3, 2, 4, 4, 9, 2, 9, 5, 8, 8, 8, 3, 1, 5, 6, 9, 0, 6, 4, 6, 3, 4, 2, 1, 7, 5, 3, 8], [1, 7, 2, 7, 7, 7, 6, 5, 3, 6, 5, 2, 6, 3, 1, 6, 1, 6, 1, 9, 
6, 0, 7, 6, 8, 6, 1, 7, 8, 5, 5, 1], [3, 6, 1, 5, 5, 6, 4, 1, 8, 6, 4, 1, 8, 2, 4, 5, 6, 6, 5, 6, 4, 7, 0, 6, 8, 7, 8, 4, 2, 4, 6, 3], [7, 6, 3, 6, 4, 9, 6, 6, 2, 4, 8, 6, 9, 8, 8, 5, 4, 5, 4, 7, 6, 6, 6, 0, 3, 4, 3, 9, 4, 8, 9, 7], [5, 2, 3, 5, 2, 6, 4, 7, 8, 5, 7, 2, 8, 3, 5, 8, 3, 2, 5, 6, 3, 8, 8, 3, 0, 8, 9, 9, 
2, 6, 7, 4], [4, 3, 2, 9, 3, 5, 8, 8, 4, 1, 9, 4, 6, 6, 2, 9, 2, 5, 3, 9, 4, 6, 7, 4, 8, 0, 6, 8, 3, 9, 8, 1], [4, 6, 4, 3, 6, 8, 7, 4, 4, 9, 3, 9, 6, 6, 8, 6, 6, 4, 3, 9, 2, 1, 8, 3, 9, 6, 0, 8, 7, 5, 9, 3], [6, 1, 6, 3, 5, 2, 1, 8, 2, 5, 6, 5, 1, 5, 8, 8, 8, 3, 3, 2, 1, 7, 4, 9, 9, 8, 8, 0, 3, 3, 4, 8], [3, 8, 8, 1, 5, 6, 1, 2, 1, 3, 2, 1, 8, 7, 2, 5, 6, 3, 8, 2, 7, 8, 2, 4, 2, 3, 7, 3, 0, 4, 6, 2], [4, 7, 6, 1, 6, 7, 
8, 9, 2, 8, 8, 6, 3, 1, 2, 6, 7, 4, 1, 8, 5, 5, 4, 8, 6, 9, 5, 3, 4, 0, 3, 9], [4, 6, 8, 8, 6, 3, 7, 9, 1, 7, 3, 3, 7, 8, 5, 4, 8, 3, 5, 3, 3, 5, 6, 9, 7, 8, 9, 4, 6, 3, 0, 2], [7, 8, 2, 7, 1, 1, 7, 2, 2, 5, 4, 4, 5, 4, 8, 8, 8, 8, 9, 6, 8, 1, 3, 7, 4, 1, 3, 8, 2, 9, 2, 0]]

print('When using Or - Tool:')
OR_Tools_solve(distance_matrix)

runtime = time.time() - before
print(f'Runtime: {runtime}')