import random as rd

n = rd.randint(5,10)
k = rd.randint(2,n-1)

def gen(filename, n, k):
    d = [[rd.randint(1, 9) for i in range(n+1)] for j in range(n+1)]
    for i in range(n+1):
        d[i][i] = 0
    f = open(filename, 'w')
    f.write(str(n)+ ' '+ str(k)+ '\n')
    for i in range(n+1):
        line = ''
        for j in range(n+1):
            line = line + str(d[i][j]) + ' '
        f.write(line + '\n')
	
gen('datanew.txt',n,k)
    
    
    
