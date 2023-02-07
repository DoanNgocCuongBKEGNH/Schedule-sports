# gibb sampling: but this method is not efficent yet
def gibb_sampling(input,K):
    best_config = None
    best_cost = float('inf')
    #initialize start position
    mat = generate(len(input))
    current_postion = (mat,compute_cost(distance_matrix,mat))
    #
    
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
mat,cost = gibb_sampling(distance_matrix,1000)
print(f'The matrix sol is {config}')
print(f'The reasonable cost when using Gibb_sampling is {cost}')
