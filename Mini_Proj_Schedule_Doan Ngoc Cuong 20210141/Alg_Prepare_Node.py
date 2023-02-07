### Alg_Prepare_Node
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

