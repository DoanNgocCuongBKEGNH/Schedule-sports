#Greedy Algorithm
import time
import math
INF = math.inf

def input(filename):
    with open(filename) as f:
        n, k = [int(x) for x in f.readline().split()]
        d = [[int(x) for x  in f.readline().split()] for i in range(n + 1)]
        return n, k, d
    
n, k , d = input('data.txt')
start_time=time.time() 
Itineraries = [[0] for i in range(k)] #itineraries of postmen 
Intineraries_length= [0]*k #length of itineraries 

def printSolution(Itineraries, Intineraries_length):
  for q in range(k):
    Intineraries_length[q] += d[Itineraries[q][-1]][0]
    Itineraries[q].append(0)
  for q in range(k):
    print('postman:' , q) 
    print('->'.join(str(i) for i in Itineraries[q]))
    print('length =', Intineraries_length[q])  
def selectPostman(): # among k postman, choose one who has shortest itinerary  
  min_length = INF
  select = -1
  for q in range(k):             
    if min_length > Intineraries_length[q]:
      min_length = Intineraries_length[q]
      select = q
  return select
def selectPoint(Candidates, q): # choose the point that is nearest the last point of itinerary q
  select = -1
  min_length = INF
  last = Itineraries[q][-1] # last point of itinerary q
  for i in Candidates :
    if min_length >  d[last][i]:
      min_length = d[last][i]
      select = i
  return select 
def first_greedy(): 
  Candidates = []
  for i in range(1, n+1):
    Candidates.append(i)
  while len(Candidates) > 0:
    q = selectPostman()
    x = selectPoint(Candidates, q)
    if x == -1 :
      print('will not pass any points')  
      break 

    last = Itineraries[q][-1]
    Intineraries_length[q] += d[last][x]
    Itineraries[q].append(x)
    Candidates.remove(x)
  printSolution(Itineraries, Intineraries_length) 
  return [sum(Intineraries_length), max(Intineraries_length)]  
x = first_greedy()
print('Sum of total length', x[0])
print('Max of length', x[1])
end_time=time.time()
print('time: ', end_time-start_time)