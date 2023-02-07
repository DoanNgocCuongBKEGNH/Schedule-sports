import random as rd
import math
def genData(filename, N, K, MAX_Q, MIN_C, MAX_C): # N số điểm, K số 
    f = open(filename, "w")
    f.write(str(N)+ ' ' + str(K) + '\n')  # dòng 1 ghi N, K

# Dòngi+1 (i= 1,..., N): ghid(i) vàc(i)•


    d = [rd.randint(1, MAX_Q) * 10 for i in range(N)]
    c = [rd.randint(MIN_C, MAX_C) for i in range(N)]
    # generate randomly a solution. 
    x = [rd.randint(K) for i in range(N)] # x[i] is the indẽx  of truck carrying the order i
    load = [0 for i in range (K)]
    c1 = [0 for k in range(K)]
    c2 = [0 for k in range(K)]

    for k in range(K): 
        for i in range(N): 
            if x[i] == k: 
                load[k] = load[k] + d[i]

    c1[k] = load[k]
    c2[k] = c1[k] + rd.randint (0, 40)

    for i in range(N): 
        f.write(str(d[i]) + ' ' + str(c[i]) + '\n')
    for k in range(K): 
        f.write(str(c1[k]) + ' ' + str(c2[k]) + '\n')

genData("pro17.txt", 10, 15, 20, 25, 30)