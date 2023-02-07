'''
optimal obj value = 7.0
( 1 , 2 )
( 2 , 4 )
( 3 , 1 )
( 4 , 3 )
'''

# print soulution 
def findNext(current): 
    for i in range(1, N  + 1): 
        if X[current][i].solution_value() > 0: 
            return i 
    return -1 # NOT FOUND 

def extractSolutionRoute(): 
    route = []
    current = 1
    route.append(1)
    for i in range(2, N + 1): 
        nextPoint = findNext(current)
        route.append(nextPoint)
        current = nextPoint
    return route

print(n)
route = extractSolutionRoute()
print(route)