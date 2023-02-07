import random as rd
import math
def genData(filename, N, K, MAX_COORDINATE): # N số điểm, K số 
    f = open(filename, "w")
    f.write(str(N)+ ' ' + str(K) + '\n')
    d = [0 for i in range(N + 1)]
    for i in range(N + 1): 
        d[i] = rd.randint(1, 5) * 10



    for i in range(1, N+1): 
        f.write(str(d[i]) + ' ')
    f.write('\n')

    x = [0 for i in range(N + 1)]
    y = [0 for j in range(N + 1)]

    for i in range(1, N + 1): 
        x[i] = rd.randint(1, MAX_COORDINATE)
        y[i] = rd.randint(1, MAX_COORDINATE)

    t = [[0 for i in range(N + 1)] for j in range(N + 1)]

    for i in range(N + 1): 
        for j in range(N + 1): 
            t[i][j] = round(math.sqrt((x[i] - x[j]) **2 +(y[i] - y[j]) **2)) # manhattan distance 
    
    for i in range(N + 1): 
        line = ''
        for j in range(N + 1): 
            line = line + str(t[i][j])  + ' '
        line = line + '\n'
        f.write(line)

genData("10.txt", 1000, 100, 100)