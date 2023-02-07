from LocalSearchManager import LocalSearchManager
from VarIntLS import VarIntLS
from NotEqual import NotEqual
from ConstraintSystem import ConstraintSystem
import random as rd

mgr = LocalSearchManager()
x = [[VarIntLS(mgr,1,9,i+1,'x['+ str(i) + ',' +str(j) + ']') for i in range (9)] for j in range(9)]

def printSolution():
    for i in range(9):
        for j in range(9):
            print(x[i][j].getValue(),end=' ')
        print('')
contraints = []
#contraints on row
for i in range(9):
    for j1 in range(8):
        for j2 in range(j1+1,9):
            c = NotEqual(x[i][j1],x[i][j2],'NotEqual')
            contraints.append(c)

#contraints on col
for i in range(9):
    for j1 in range(8):
        for j2 in range(j1+1,9):
            c = NotEqual(x[j1][i],x[j2][i],'NotEqual')
            contraints.append(c)
#contraints on sub-square

for I in range(3):
    for J in range(3):
        for i1 in range (3):
            for i2 in range(3):
                for j1 in range(3):
                    for j2 in range(3):
                        if i1 != i2 or j1 != j2:
                            c = NotEqual(x[3*I+i1][3*J+j1],x[3*I+i2][3*J+j2],'NotEqual')
                            contraints.append(c)
C = ConstraintSystem(contraints)

mgr.close() #close the model

#perform local search (hill climbing)
#make use of C.getAssigndelta,C.getSwapDelta for neighborhood query

def simpleHillClimbing(maxIters):
    #explore all possible assignment (x[i][j] <- v)
    for it in range(maxIters):
        #explore neighborhood for finding the best neighborhood solution
        minDelta = 1e9
        select_i = -1
        select_j = -1
        select_value = -1
        candidates = []
        for i in range(9):
            for j in range(9):
                for v in range(1,10):
                    delta = C.getAssignDelta(x[i][j],v)
                    if delta < minDelta:
                        minDelta = delta
                        candidates = []
                        candidates.append([i,j,v])
                    elif delta == minDelta:
                        candidates.append([i,j,v])
        #select ramdomly an ele from candidates
        idx = rd.randint(0,len(candidates)-1)
        select_i = candidates[idx][0]
        select_j = candidates[idx][1]
        select_value = candidates[idx][2]
        # perform the selected local move
        x[select_i][select_j].setValuePropagate(select_value)
        print('step',it,'x[',select_i,',',select_j,'] ='.select_value,' violations = ',C.violations)
        if C.violations() == 0:
            break

def improveHillClimbing(maxIters):
    for it in range(maxIters):
        candidates = []
        minDelta = 1e9
        for i in range(9):
            for j1 in range(8):
                for j2 in range(j1+1,9):
                    delta = C.getSwapDelta(x[i][j1],x[i][j2])
                    if delta < minDelta:
                        minDelta = delta
                        candidates = []
                        candidates.append([i,j1,j2])
                    elif delta == minDelta:
                        candidates.append([i,j1,j2])
        idx = rd.randint(0,len(candidates)-1)
        i = candidates[idx][0]
        j1 = candidates[idx][1]
        j2 = candidates[idx][2]
        x[i][j1].swapValuePropagate(x[i][j2]) # perform local move by swapping 2 ele var
        print('Step ',it,'swap[',i,',',j1,'] and x[',i,',',j2,'] violations = ', C.violations())
        if C.violations() == 0:
            break
        


print('Init, C = ',C.violations())
improveHillClimbing(2000)
printSolution()
