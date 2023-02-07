#Greedy Algorithm
INF = 1e9
N = 1000

def input(filename):
    with open(filename) as f:
        n, k = [int(x) for x in f.readline().split()]
        d = [[int(x) for x  in f.readline().split()] for i in range(n + 1)]
        return n, k, d
    
n, k , d = input('data.txt')
P = []
for i in range(k):
  P.append([0]) #itineraries of postmen 
F = [0]*k #length of itineraries 

def printSolution():
  for q in range(k):
    F[q] += d[P[q][-1]][0]
    P[q].append(0)
  for q in range(k):
    print('postman:' , q) 
    print('->'.join(str(i) for i in P[q]))
    print('length =', F[q])  
def selectPostman(): # among k postman, choose one who has the shortest itinerary 
  minF = INF
  select = -1
  for q in range(k):             
    if minF > F[q]:
      minF = F[q]
      select = q
  return select
def selectPoint(Candidate, q): # choose the point that is nearest the last point of itinerary q
  select = -1
  minF = INF
  last = P[q][-1] # last point of itinerary q
  for i in Candidate :
    if minF >  d[last][i]:
      minF = d[last][i]
      select = i
  return select 
def greedy1(): 
  Candidate = []
  for i in range(1, n+1):
    Candidate.append(i)
  while len(Candidate) > 0:
    q = selectPostman()
    x = selectPoint(Candidate, q) 

    last = P[q][-1]
    F[q] += d[last][x]
    P[q].append(x)
    Candidate.remove(x)
  printSolution()    
greedy1()  