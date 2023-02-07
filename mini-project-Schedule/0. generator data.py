import random as rd

n = rd.randint(2, 30, 2)

def gen(filename, n):
    d = [[rd.randint(1, 9) for i in range(n+1)] for j in range(n+1)]
    for i in range(n+1):
        d[i][i] = 0
    for i in range(n+1): 
        for j in range(n+1): 
            d[i][j] = d[j][i]
    '''
    •Input
    •Dòng1: ghi số nguyên dương N
    •Dòngi+1 (i= 1,..., N): ghi hàng thứ i của ma trận d   
    < Khoảngcáchtừsâncủađộituyểniđếnsâncủađộituyểnj là d(i,j).>
    '''        
    # file object = open(file_name [, access_mode][, buffering])
    f = open(filename, 'w')
    f.write(str(n)+ '\n')
    for i in range(n):
        line = ''      
        for j in range(n):
            line += str(d[i][j]) + ' '
        f.write(line + '\n')
	
gen('datanew.txt',n)
    
    
    
