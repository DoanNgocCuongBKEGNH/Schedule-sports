import math
import copy
import time


def read_data(filename):
    with open(filename) as f:
        n, k = [int(x) for x in f.readline().split()]
        d = [[int(x) for x  in f.readline().split()] for i in range(n + 1)]
        return n, k, d
    
    
def part(n, k):
    def _part(n, k, pre):
        if n <= 0:
            return []
        if k == 1:
            if n <= pre:
                return [[n]]
            return []
        ele = []
        for i in range(min(pre, n), 0, -1):
            ele += [[i] + sub for sub in _part(n-i, k-1, i)]
        ele.reverse()
        return ele
    return _part(n, k, n)
    

def visited(j,m):
    for i in range(1,m):
        if (j == arr[i]):
            return False
    return True


def position(m):
    next = 0
    curr = 0
    for i in range(len(depot)):
        if (depot[i] < m) and (m <= depot[i+1]):
            next = depot[i + 1]
            curr = i
            break
    return next, curr 
    
    
def BnB(m):
    global f, r, a_opt, f_opt, r_opt
    next_depot, curr_postman = position(m) 
    for j in range(1,n+1):
        if (visited(j,m)):
            temp1 = f
            temp2 = r
            if m not in depot:
                arr[m] = j
                r += d[arr[m-1]][arr[m]]
            else:
                r += d[arr[m-1]][arr[m]]
                path[curr_postman] = r 
                r = 0
            f += d[arr[m-1]][arr[m]]
            if m == n+k-1:
                path[curr_postman] = r + d[arr[m]][arr[m+1]]
                r_final = max(path)
                f_final = f
                f_final = f+ d[arr[n+k-1]][arr[n+k]]
                if (f_final < f_opt):
                    a_opt = copy.deepcopy(arr)
                    f_opt = f_final
                    r_opt = r_final
            else:
                g1 = f + (n+k-m+2)*dmin
                if m not in depot:
                    g2 = r + (next_depot - m)*dmin
                else: 
                    g2 = path[curr_postman]
                if (g1 < f_opt) and (g2 < r_opt):
                    BnB(m+1)
            f = temp1
            r = temp2

 

def printSolution():
    route = []
    sub = []
    for i in range(1, len(a_opt)):
        if a_opt[i] != 0:
            sub.append(a_opt[i])
        else:
            route.append(sub)
            sub = []
    for q in range(k):
        print('Route ['+str(q)+']: 0 -> ', end = '')
        for i in route[q]:
            print(str(i) + ' -> ', end = '')
        print('0')
    print('Objective 1 =', r_opt)
    print('Objective 2 =', f_opt)
    print('Time =', end-start)  
    
      
if __name__ == '__main__':
    n, k, d = read_data('data7.txt')
    dmin = min(d[i][j] for i in range(n+1) for j in range(n+1) if i != j)
    f_opt = math.inf
    r_opt = math.inf
    a_opt = []
    f = 0
    route_opt = []
    start = time.time()

    for num in part(n,k):
        arr = [0]*(n+k+1)
        path = [0]*k
        depot = [0]
        r = 0
        idx = 0
        for q in range(k):
            idx += num[q] + 1
            depot.append(idx)
        BnB(1)
    end = time.time()
    
    printSolution()   
