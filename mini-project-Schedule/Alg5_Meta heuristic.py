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
mat,cost = iterative_local_solve(distance_matrix,K=100)
print(f'The matrix sol is {mat}')
print(f'The reasonable cost when using Iterative Local Search is {cost}')