from VarIntLS import VarIntLS
from LocalSearchManager import LocalSearchManager
from NotEqual import NotEqual
from ConstraintSystem import ConstraintSystem
import random as rd

mgr = LocalSearchManager()
#defind decision varibles
x = [VarIntLS(mgr,1,9,i+1,'x[' + str(i) + ',' + str(j)+ ']') for i in range(9) for j in range(9)]
constraints = []

def printSolution():
	for i in range(9):
		for j in range(9): 
			print(x[i][j].getValue(), end = ' ')
		print('')

#constraint on rows 
for i in range(9): 
	for j1 in range(8): 
		for j2 in range(j1+1, 9): 
			c = NotEqual(x[i][j1], x[1][j2], 'NotEqual')
			constraints.append(c)

#constraint on columns
for i in range(9): 
	for j1 in range(8): 
		for j2 in range(j1+1, 9): 
			c = NotEqual(x[i1][j], x[i2][j], 'NotEqual')
			constraints.append(c)

#constraint on rows 
for I in range(3): 
	for J in range(3): 
		for i1 in range(3):
			for j1 in range(3): 
				for i2 in range(3): 
					for j2 in range(3): 
						if i1 != i2 or j1 != j2:
							c = NotEqual(x[3*I + i1][3*J + j1], x[3*I + i2][3*J + j2], 'NotEqual')
							constraints.append(c)


C = ConstraintSystem(constraints)
mgr.close() #close the model, init data structures representing relation between components of them. 

def simpleHillClimbing(): 
	# explore all 
	for it in range(maxIters): 
		minDelta = le9
		select_i = - 1
		selectj = -1 
		select_value = -1 
	for i in range(9): 
		for j in range(9): 
			for v in range(1, 10): 
				delta = C.getAssignDelta(x[i][j], v)
				if delta < minDelta: 
					minDelta = delta
					candidates = []
					candidates.append([i, j, v])
				elif delta == minDelta: 
	     			candidates.append([i, j, v])
	# select randomlyy an elements from candidates
	idx = rd.randint(0,len(candidaes) - 1)
	select_i = candidates[idx][0]
	select_j = candidates [idx][1]
	select_value  = candidates [idx][1]
	# perform the selected local move 
	x[select_i][select_j].setValuePropagate(select_value)
	print('step', it, 'x[', select_i, ',', select_j, '] =', select_value, 'violations =', C.violations())
# van ko thoat ra duoc khoi toi uu cuc bo du da dua vo list -> random 
def improveHilllimbing(maxIters): 
	for it in range(maxIters): 
		candidates = []
		for i in range(9): 
			for j1 in rang (8): 
				for j2 in range ( j1 + 1, 9): 
					delta = C.getSwapDelta(x[i][j1], x[i], [j2])
					if delta < minDelta: 
						candodates = []
						candidates.append(i, j1, j2)
					elif delta == minDelta: 
						candidates.appent(i, j1, j2)
		idx = rd.randint(0, len(candidates) -1)
		i = candidates[idx][0]
		j1 = candidates[idx][1]
		j2 = candtidates [idx][2]
		x[i][j].swapValuePropagate(x[i][j2])
		print('step', it, 'swap x[', i, ',', j1, '] an x[',i, ',', j2)
print('Init, c =', c.violations())
printSolution()