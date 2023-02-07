import time
before = time.time()

import copy
from Alg_Prepare_Node import Node, get_sub_node

def find_min(matrix:list):
    ans = float('inf')
    for row in matrix:
        for entry in row:
            if entry != 0 and entry < ans:
                ans = entry
    return ans

### BeamSearch algorithm ###
def beam_search_solve(input,k):
    N = len(input)
    queue = []
    ## tracking the best value in the tree
    c_min = find_min(input)

    ##
    ##initialize the root of the tree.
    root_matrix = [[None for i in range(N)] for i in range(N)]
    for i in range(N):
        root_matrix[i][i] = 0
    root_distance = 0
    week = 0
    root_tracking_pos = [i for i in range(N)]
    root = Node(root_matrix,root_distance,week,root_tracking_pos)
    queue.append(root)
    best = None
    
    while True:
        nodes = copy.deepcopy(queue) 
        queue = []
        if nodes[0].week == 2*N - 2:
            for node in nodes:
                if best == None:
                    best = node.matrix,node.distance
                else:
                    if node.distance < best[1]:
                        best = node.matrix,node.distance
            break
        else:
            next_week = nodes[0].week + 1
            for node in nodes:
                lis = get_sub_node(input,node)
                sub_nodes = [Node(sub_matrix,sub_distance,next_week,sub_pos) for \
                    (sub_matrix,sub_pos,sub_distance) in lis]
                queue += sub_nodes
            queue = sorted(queue,key=lambda x: x.distance)[:k]

    return best
distance_matrix = [[0, 1, 2, 3], [1, 0, 4, 5], [2, 4, 0, 6], [3, 5, 6, 0]]
distance_matrix = [[0, 9, 4, 7, 9, 7], [9, 0, 2, 1, 4, 8], [4, 2, 0, 5, 7, 2], [7, 1, 5, 0, 9, 3], [9, 4, 7, 9, 0, 6], [7, 8, 2, 3, 6, 0]]
distance_matrix = [[0, 9, 3, 9, 8, 5, 3, 1, 4, 1], [9, 0, 4, 6, 8, 4, 9, 7, 8, 8], [3, 4, 0, 3, 1, 2, 5, 5, 3, 9], [9, 6, 3, 0, 7, 9, 6, 1, 7, 1], [8, 8, 1, 7, 0, 7, 6, 3, 5, 7], [5, 4, 2, 9, 7, 0, 1, 4, 8, 5], [3, 9, 5, 6, 6, 1, 
0, 1, 8, 2], [1, 7, 5, 1, 3, 4, 1, 0, 9, 7], [4, 8, 3, 7, 5, 8, 8, 9, 0, 8], [1, 8, 9, 1, 7, 5, 2, 7, 8, 0]]
config_beam_search,val_beam_search = beam_search_solve(distance_matrix,10) 
print(f'The reasonable cost when using Beam Search is {val_beam_search}, when: matrix is {config_beam_search}')


runtime = time.time() - before
print(f'Runtime: {runtime}')