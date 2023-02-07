from Alg1_BackTracking_copy import Node, get_sub_node

### Greedy Search ###
def greedy_solve(input:list):
    N = len(input)
    queue = []
    ##initialize the root of the tree.
    root_matrix = [[None for i in range(N)] for i in range(N)]
    for i in range(N):
        root_matrix[i][i] = 0
    root_distance = 0
    week = 0
    root_tracking_pos = [i for i in range(N)]
    root = Node(root_matrix,root_distance,week,root_tracking_pos)
    queue.append(root)
    while queue:
        temp = queue.pop()
        assert isinstance(temp, Node)

        current_week = temp.week
        if current_week == 2*N - 2:
            return (temp.matrix,temp.distance)
        else:
            next_week = current_week + 1
            list_of_nodes = get_sub_node(input,temp)
            #node: sub_matrix,sub_pos,sub_distance
            new_list = sorted(list_of_nodes,key=lambda x:x[2])
            sub_matrix,sub_pos,sub_distance = list_of_nodes[0]
            new_node = Node(sub_matrix,sub_distance,next_week,sub_pos)
            queue.append(new_node)
distance_matrix = [[0, 1], [3, 0]]
mat,cost = greedy_solve(distance_matrix)
print(f'Matrix {mat}')
print(f'The reasonable cost when using Greedy Search is {cost}')