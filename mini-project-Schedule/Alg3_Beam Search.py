### BeamSearch algorithm ###
def beam_solve(input,k):
    N = len(input)
    queue = []
    ## tracking the best value in the tree
    c_min = find_min(input)

    ##
    ##initialize the root of the tree.
    root_matrix = [[None for i in range(N)] for i in range(N)]
    for i in range(N):
        root_matrix[i][i] = 0
    root_dis = 0
    week = 0
    root_tracking_pos = [i for i in range(N)]
    root = Node(root_matrix,root_dis,week,root_tracking_pos)
    queue.append(root)
    best = None
    
    while True:
        nodes = copy.deepcopy(queue) 
        queue = []
        if nodes[0].week == 2*N - 2:
            for node in nodes:
                if best == None:
                    best = node.matrix,node.dis
                else:
                    if node.dis < best[1]:
                        best = node.matrix,node.dis
            break
        else:
            next_week = nodes[0].week + 1
            for node in nodes:
                lis = get_sub_node(input,node)
                sub_nodes = [Node(sub_matrix,sub_dis,next_week,sub_pos) for \
                    (sub_matrix,sub_pos,sub_dis) in lis]
                queue += sub_nodes
            queue = sorted(queue,key=lambda x: x.dis)[:k]

    return best

config,val = beam_solve(distance_matrix,10) 
print(f'The matrix sol is {config}')
print(f'The reasonable cost when using Beam Search is {val}')