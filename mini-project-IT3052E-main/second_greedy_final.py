import time
import math
INF = math.inf
#Greedy 2 Algorithm

def input(filename):
    with open(filename) as f:
        n, k = [int(x) for x in f.readline().split()]
        d = [[int(x) for x  in f.readline().split()] for i in range(n + 1)]
        return n, k, d
    
n, k , d = input('data.txt')

start_time=time.time() 
Itineraries = [[0] for i in range(k)] #itineraries of postmen 
Intineraries_length = [0]*k #length of itineraries 

def printSolution():
  for q in range(k):
    Intineraries_length[q] += d[Itineraries[q][-1]][0]
    Itineraries[q].append(0)
  for q in range(k):
    print('postman:' , q) 
    print('->'.join(str(i) for i in Itineraries[q]))
    print('length =', Intineraries_length[q])  
 
def selectPostmanPoint(Candidate2): #choose the best greedy pair of Postman and Point
  select_q = -1
  select_i = -1 
  min_length = INF
  for q in range(k) :
    for i in Candidate2:
      last = Itineraries[q][-1]
      max_length = Intineraries_length[q] + d[last][i]
      for j in range(k):
        if j != q and max_length < Intineraries_length[j]:
            max_length = Intineraries_length[j]
      if min_length > max_length :
        min_length = max_length 
        select_q = q
        select_i = i
  return (select_q, select_i)

def second_greedy():
  Candidate2 = []
  for i in range(1, n+1):
    Candidate2.append(i)
  while len(Candidate2) > 0:
    q, x = selectPostmanPoint(Candidate2)
    last = Itineraries[q][-1]
    Intineraries_length[q] += d[last][x]
    Itineraries[q].append(x)
    Candidate2.remove(x)
  printSolution() 
  return [sum(Intineraries_length), max(Intineraries_length)]  
x = second_greedy()
print('Sum of total length', x[0])
print('Max of length', x[1])
end_time=time.time()
print('time: ', end_time-start_time)  