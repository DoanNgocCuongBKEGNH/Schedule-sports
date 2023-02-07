import random as rd

def gen(filename, n):
    distance_matrix = [[rd.randint(1, 9) for i in range(n)] for j in range(n)]
    for i in range(n):
        distance_matrix[i][i] = 0
    for i in range(n): 
        for j in range(n): 
            distance_matrix[i][j] = distance_matrix[j][i]
    print(distance_matrix)    # print matrix
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
            line += str(distance_matrix[i][j]) + ' '
        f.write(line + '\n')

n = 6
gen('datanew.txt',n)

    
    
    
