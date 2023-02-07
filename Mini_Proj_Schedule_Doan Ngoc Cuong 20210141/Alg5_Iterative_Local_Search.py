# Alg5_Iterative_Local_Search

# Meta heuristic algorithm 
# -> Phần 1: Iterative Local Search
# -> Phần 2: Gibb Sampling
import time
before = time.time()

from Alg4_Local_Search import local_solve

# iterative local search #
def iterative_local_solve(input,K):
    best_config = None
    best_cost = float('inf')
    for i in range(K):
        matrix,cost = local_solve(input)
        if cost < best_cost:
            best_cost = cost
            best_config = matrix

    return best_config,best_cost


distance_matrix = [[0, 1, 2, 3], [1, 0, 4, 5], [2, 4, 0, 6], [3, 5, 6, 0]]
distance_matrix = [[0, 9, 4, 7, 9, 7], [9, 0, 2, 1, 4, 8], [4, 2, 0, 5, 7, 2], [7, 1, 5, 0, 9, 3], [9, 4, 7, 9, 0, 6], [7, 8, 2, 3, 6, 0]]
# mat_iter_local_search,cost_iter_local_search = iterative_local_solve(distance_matrix,K=100)
print(f'The reasonable cost when using Iterative Local Search is {cost_iter_local_search}, when: matrix is {mat_iter_local_search}')


runtime = time.time() - before
print(f'Runtime: {runtime}')