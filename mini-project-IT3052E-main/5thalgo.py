from python_tsp.exact import solve_tsp_dynamic_programming
import numpy as np
import time
def input(filename):
    with open(filename) as f:
        n,k = [int(x) for x in f.readline().split()]
        d=[]
        for i in range(n+1):
            li = [int(x) for x in f.readline().split()]
            li.append(li[0])
            d.append(li)
    return n,k,d
n,K,d=input('input.txt')
start_time=time.time() 

def sorted_k_partitions(seq, k):
    n = len(seq)
    groups = []  # a list of lists, currently empty
    def generate_partitions(i):
        if i >= n:
            yield list(map(tuple, groups))
        else:
            if n - i > k - len(groups):
                for group in groups:
                    group.append(seq[i])
                    yield from generate_partitions(i + 1)
                    group.pop()
            if len(groups) < k:
                groups.append([seq[i]])
                yield from generate_partitions(i + 1)
                groups.pop()
    result = generate_partitions(0)
    result = [sorted(ps, key = lambda p: (len(p), p)) for ps in result]
    result = sorted(result, key = lambda ps: (*map(len, ps), ps))
    return result
list_of_point=[x for x in range(1,n+1)]
possible_divisions=sorted_k_partitions(list_of_point,K)

#Main
MIN,solution,result_list=1000000000,1000000000,[]
for division in possible_divisions:
    max, total_cost,path =0, 0, [] 
    for k in division:
        point_list=[0]+[x for x in k]
        adj=[]
        for i in point_list:
            li=[d[i][j] for j in point_list]
            adj.append(li)        
        distance_matrix=np.array(adj)
        final_path, final_res = solve_tsp_dynamic_programming(distance_matrix)
        total_cost+=final_res
        path.append(final_path)
        if final_res>max: #max of the salesman
            max=final_res
    
    if max<MIN:
        MIN=max
        path_list=path
        solution=total_cost
        result_list=division
    elif max==MIN and (total_cost<solution):
        path_list=path
        solution=total_cost
        result_list=division

print(solution)
end_time=time.time()
for i in range(len(path_list)):
    for j in range(1,len(path_list[i])):
        path_list[i][j]=result_list[i][path_list[i][j]-1]
    path_list[i]+=[0]
for i in path_list:
    new_path='->'.join([str(x) for x in i])
    print(new_path)
print('time: ', end_time-start_time)
