### BackTracking ###
import copy

class Node():
    def __init__(self,matrix:list,distance,week,tracking_pos) -> None:
        self.matrix = matrix
        self.distance = distance
        self.week = week
        self.tracking_pos = tracking_pos                 

def get_sub_node(distance_matrix,node:Node):
    """ returns the list contains all tuples: (matrix,pos,distance) """
    ans_matrix = []
    final_ans = []
    queue = [(node,0)]
    current_week = node.week + 1
    N = len(distance_matrix)
    assert N%2 == 0, "The number of teams must be even"
    while queue:
        temp,match = queue.pop()
        matrix = temp.matrix
        pos = temp.tracking_pos
        distance = temp.distance
        if match == N//2:
            if temp.matrix not in ans_matrix:
                ans_matrix.append(temp.matrix)
                final_ans.append((temp.matrix,temp.tracking_pos,temp.distance))
        else:
            for i in range(N):
                if current_week not in matrix[i] and current_week not in [matrix[j][i] for\
                    j in range(N)]:
                    for j in range(N):
                        if i!=j and current_week not in matrix[j] and current_week not \
                            in [matrix[i][j] for i in range(N)]:
                            if matrix[i][j] == None:
                                sub_matrix = copy.deepcopy(matrix)
                                sub_matrix[i][j] = current_week
                                sub_pos = copy.deepcopy(pos)
                                sub_pos[i],sub_pos[j] = j,j
                                sub_distance = distance + distance_matrix[pos[i]][j] + distance_matrix[pos[j]][j]
                                sub_Node = Node(sub_matrix,sub_distance,current_week,sub_pos)
                                queue.append((sub_Node,match+1))
    return final_ans

def backtrack_solve(input:list):
    N = len(input) # N
    queue = []     # initial queue empty
    ## tracking the best distance in the tree
    best_distance = float('inf')
    best_config = None
    #initial the root of the tree
    root_matrix = [[None for i in range(N)] for i in range(N)]
    for i in range(N):
        root_matrix[i][i] = 0     # Đường chéo chính  = 0
    root_distance = 0     # initial root_distance
    week = 0      # initial week
    root_tracking_pos = [i for i in range(N)]
    root = Node(root_matrix,root_distance,week,root_tracking_pos)

    queue.append(root)
    

    while queue:   # matrix, distance
        temp = queue.pop()     #stack: a, b, c -> pop(0): a, pop(): c
        assert isinstance(temp, Node)  # Not assertIsInstance in unittest - khẳng định là trường hợp
        current_week = temp.week
        if current_week == 2*N - 2:
            if temp.distance < best_distance:
                best_config = temp.matrix
                best_distance = temp.distance
                print(f"Found better configuration, the new best distance is : {best_distance}")
                print(f"The new best config is {best_config}")
                print(f"number week {temp.week}")
                print(f"The Tracking_pos {temp.tracking_pos}")
                print()

        else: # if current_week not 2N - 2
            next_week = current_week + 1    # +1 week
            list_of_nodes = get_sub_node(input,temp)
            for item in list_of_nodes:
                sub_matrix,sub_pos,sub_distance = item
                if sub_distance < best_distance:
                    sub_Node = Node(sub_matrix,sub_distance,next_week,sub_pos)
                    queue.append(sub_Node)

# distance_matrix = [[0, 1], [3, 0]]
# distance_matrix = [[0, 1, 2], [1, 0, 3], [2, 3, 0]] # AssertionError: The number of teams must be even
distance_matrix = [[0, 1, 2, 3], [1, 0, 4, 5], [2, 4, 0, 6], [3, 5, 6, 0]]

backtrack_solve(input=distance_matrix)
# The new best config is [[0, 6, 2, 1], [3, 0, 1, 2], [5, 4, 0, 3], [4, 5, 6, 0]]
# 0, 6, 2, 1
# 3, 0, 1, 2
# 5, 4, 0, 3
# 4, 5, 6, 0