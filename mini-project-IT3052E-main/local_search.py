import random as rd
import copy

def input(filename):
    '''
    Read input data function'''
    with open(filename) as f:
        n, k = [int(x) for x in f.readline().split()]
        d = [[int(x) for x  in f.readline().split()] for i in range(n + 1)]
        for i in range(n+1):
            d[i].append(d[i][0])
        return n, k, d
#defining functions 
def findnext(Kc: list, path: list, length, i, d):
    '''
    Find the next point in the path'''
    Ai = [j for j in range(1, n+2) if j!= i and (i,j) != (0, n+1)]
    lst = [d[i][j] for j in Ai if j in Kc]
    minn = min(lst)
    length += minn
    nextt = Kc[lst.index(minn)]
    Kc.remove(nextt)
    path.append(nextt)
    return Kc, path, length

def findpath(Kc, d):
    '''
    TSP greedy function find the path knowing the point list'''
    path = [0]
    length = 0
    con = True
    while con:
        if len(Kc) == 1:
            length += d[path[-1]][Kc[0]]
            length += d[Kc[0]][0]
            path.append(Kc[0])
            path.append(0)
            con = False
        else:
            Kc, path, length = findnext(Kc, path, length, path[-1], d)         
    return path, length  

def switch(K, allpath, len_lst, maxx, minn, opt, sum_opt, d):
    '''
    Switch a point from the max path to the min path'''
    op = opt
    sum_op = sum_opt
    for x in K[maxx]:
        Kcopy = copy.deepcopy(K)
        apath = copy.deepcopy(allpath)
        ll = copy.deepcopy(len_lst)
        Kcopy[maxx].remove(x)
        Kcopy[minn].append(x)
        apath[maxx], ll[maxx] = findpath(Kcopy[maxx], d)
        apath[minn], ll[minn] = findpath(Kcopy[minn], d)
        sum_temp = sum(ll)
        temp = max(ll)
        if temp < opt or (temp == opt and sum_temp < sum_opt):
            opt = temp
            Krs = copy.deepcopy(Kcopy)
            rspath = copy.deepcopy(apath)
            rslen = copy.deepcopy(ll)
            sum_opt = sum_temp
    if opt == op and sum_opt == sum_op:
        return False, None, None, None, None
    else:
        return True, rspath, rslen, opt, sum_opt 
    
def better(K: list, allpath: list, len_lst: list, d):
    '''
    Try to get better solution'''   
    opt = max(len_lst)
    sum_opt = sum(len_lst)
    maxx = len_lst.index(opt)
    if len(K[maxx]) == 1: #no better solution
        return False, None, None, None, None
    mi = min(len_lst)
    if mi == opt:
        return False, None, None, None, None
    minn = len_lst.index(mi)
    cont, nallpath, nlen_lst, nopt, nsopt = switch(K, allpath, len_lst, maxx, minn, opt, sum_opt, d)
    return cont, nallpath, nlen_lst, nopt, nsopt

def print_result(allpath, len_lst, opt, sum_opt):
    '''
    This function print out the current solution'''
    m = len(len_lst)
    print('Maximum distance:', opt) 
    print('Total distance:', sum_opt) 
    for q in range(m):
        s = '0->'
        l = len(allpath[q])
        for i in range(1, l):
            if i != l-1:
                s += str(allpath[q][i])
                s += '->'
            if i == l-1:
                s += str(0)
        print(f'Postman[{q}], Length: {len_lst[q]}, Route: {s}')
    print()
    
def local_search(n,k,d):
    '''
    Local search function to solve the problem with random starting solution
    Print out the acceptable solution reached'''     
    #start randomly
    cont = True
    while cont:
        K = [[] for q in range(k)]
        N = dict()
        cont = False
        for i in range(1, n+1):
            N[i] = rd.randint(0,k-1)
            K[N[i]].append(i)
        for q in range(k):
            if len(K[q]) == 0:
                cont = True
    allpath = []
    len_lst = []
    for q in range(k):
        Kc = [i for i in K[q]]
        path, length = findpath(Kc, d)
        allpath.append(path)
        len_lst.append(length)
    opt = max(len_lst)
    sum_opt = sum(len_lst)
    print('START')
    print_result(allpath, len_lst, opt, sum_opt)
    #find better solutions
    cont = True
    j = 0
    while cont:
        j += 1
        cont, a, b, c, u = better(K, allpath, len_lst, d)
        if cont:
            allpath = a
            len_lst = b
            opt = c
            sum_opt = u
            K = [[i for i in x if i!=0] for x in allpath]
            print(f'UPDATE({j})')
            print_result(allpath, len_lst, opt, sum_opt)
    #print final result
    print('FINAL RESULT')        
    print_result(allpath, len_lst, opt, sum_opt)
            
if __name__ == '__main__': 
    n, k , d = input('data1.txt')      
    local_search(n,k,d)
        
        
    
      

    

