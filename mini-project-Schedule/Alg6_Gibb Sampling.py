# Alg6_Gibb Sampling

# Meta heuristic algorithm 
# -> Phần 1: Iterative Local Search
# -> Phần 2: Gibb Sampling

import time
before = time.time()

import random
from Alg4_Local_Search import generate, compute_cost, get_neighbors

# gibb sampling: but this method is not efficent yet
def gibb_sampling(input,K):
    best_config = None
    best_cost = float('inf')
    #initialize start position
    mat = generate(len(input))
    current_postion = (mat,compute_cost(distance_matrix,mat))
    
    for i in range(K):
        #choosing a random number:
        num = random.random()

        list_of_neighs = get_neighbors(current_postion) #mat,cost
        sum_of_cost = sum(x[1] for x in list_of_neighs)
        accumulate = 0
        for i in range(len(list_of_neighs)):
            mat,cost = list_of_neighs[i]
            accumulate += cost
            port = accumulate / sum_of_cost
            if port > num:
                current_postion = list_of_neighs[i-1]
                break
    return current_postion

distance_matrix = [[0, 1, 2, 3], [1, 0, 4, 5], [2, 4, 0, 6], [3, 5, 6, 0]]    
mat_gibb_sampling,cost_gibb_sampling = gibb_sampling(distance_matrix,1000)
print(f'The reasonable cost when using Gibb_sampling is {cost_gibb_sampling}, when: matrix is {mat_gibb_sampling}')

runtime = time.time() - before
print(f'Runtime: {runtime}')