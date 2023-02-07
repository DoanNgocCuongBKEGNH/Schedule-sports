import random
def GetData(filename,n,K,M,MaxSizeC,MaxSizeI,MaxC):
    f = open(filename,'w')
    f.write(str(n)+' '+str(K)+'\n') 
    w = [0 for i in range(n)]
    l = [0 for i in range(n)]
    W = [0 for i in range(n)]
    L = [0 for i in range(n)]
    c = [0 for i in range(n)]

    for i in range(n):
        w[i] = random.randint(1,MaxSizeI)
        l[i] = random.randint(1,MaxSizeI)
    
    MaxW = max(w)
    MaxL = max(l)

    for k in range(K):
        W[k] = random.randint(MaxW,MaxSizeC)
        L[k] = random.randint(MaxW,MaxSizeC)
        c[k] = random.randint(MaxC//2,MaxC)
    
    for i in range(n):
        f.write(str(w[i])+' '+str(l[i])+'\n')
    for k in range(K):
        f.write(str(W[k])+' '+str(L)+' '+str(c[k])+'\n')

GetData('3.txt',10,5,20,100,50,60)