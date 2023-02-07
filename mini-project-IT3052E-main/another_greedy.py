#Greedy 2 Algorithm
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
F = [0]*k #length off itineraries 

def printSolution():
  for q in range(k):
    F[q] += d[P[q][-1]][0]
    P[q].append(0)
  for q in range(k):
    print('postman:' , q) 
    print('->'.join(str(i) for i in P[q]))
    print('length =', F[q])  
 
def selectPostmanPoint(Candidate2): #choose the best greedy pair of Postman and Point
  select_q = -1
  select_i = -1 
  minF = INF
  for q in range(k) :
    for i in Candidate2:
      last = P[q][-1]
      max_length = F[q] + d[last][i]
      for j in range(k):
        if j != q and max_length < F[j]:
            max_length = F[j]
      if minF > max_length :
        minF = max_length 
        select_q = q
        select_i = i
  return (select_q, select_i)

def greedy2():
  Candidate2 = []
  for i in range(1, n+1):
    Candidate2.append(i)
  while len(Candidate2) > 0:
    q, x = selectPostmanPoint(Candidate2)
    last = P[q][-1]
    F[q] += d[last][x]
    P[q].append(x)
    Candidate2.remove(x)
  printSolution()  
greedy2()    
