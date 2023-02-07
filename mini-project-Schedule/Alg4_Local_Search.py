import time
before = time.time()

### Local Search ###
import traceback
import random
import numpy 
import copy

def generate(N):

    mat_0 = list()
    for i in range(N):
        row = [None]*N
        row[i] = 0
        mat_0.append(row)

    all_coors_0 = list((a,b) for a in range(0,N) for b in range(0,N))
    for i in range(N):
        all_coors_0.remove((i,i))

    n_choices_0 = dict()
    choices_0 = dict()
    for i in range(1,N+1):
        n_choices_0[i] = N-1
        choices_0[i] = [a for a in range(1,N+1) if a != i]
    
    univ_tab = dict()

    univ_tab[0] = [copy.deepcopy(n_choices_0), copy.deepcopy(choices_0), copy.deepcopy(all_coors_0), copy.deepcopy(mat_0)]

    global result
    result = []

    def construct_mat(n):
        global result
        if n == 2*N - 2:
            result = univ_tab[n][3]
        else:
            nextweek = construct_week(n+1)
            if nextweek == False:
                construct_mat(n)
            elif nextweek == 'Reset':
                construct_mat(n-1)
            else:
                univ_tab[n+1] = copy.deepcopy(nextweek)
                construct_mat(n+1)

    # functions for contructing week 

    def create_priority_queue(n_choices_f):
        L = list()
        for a,b in n_choices_f.items():
            L.append((b,a))

        L.sort()

        Q = list()
        for item in L:
            Q.append(item[1])
        return Q

    def check_choices(choices_copy):
        L = list()
        for key in choices_copy.keys():
            if len(choices_copy[key]) == 0:
                L.append(key)
        for key in L:
            choices_copy.pop(key)

    def create_n_choices(choices):
        n_choices_f = dict()
        for key in choices.keys():
            n_choices_f[key] = len(choices[key])
        
        return n_choices_f
    def choose_match(a: int, n_choices: dict, choices: dict, choices_copy: dict, all_coors: list, rest: list, queue: list, mat: list, week: int, p_queue: list, b = None):
        
        if b == None:
            b = random.choice(choices_copy[a])

        rest.remove(a)
        rest.remove(b)
        queue.remove(a)
        queue.remove(b)
        p_queue = copy.deepcopy(queue)

        for key in choices_copy.keys():
            if a in choices_copy[key]:
                choices_copy[key].remove(a)
            if b in choices_copy[key]:
                choices_copy[key].remove(b)
        choices_copy.pop(a)
        choices_copy.pop(b)

        RC = []
        if (a-1,b-1) in all_coors:
            RC.append((a,b))
        if (b-1,a-1) in all_coors:
            RC.append((b,a))
        
        (c,d) = random.choice(RC)

        all_coors.remove((c-1,d-1))

        if len(RC) == 1:
            n_choices[a] -= 1
            n_choices[b] -= 1
            choices[a].remove(b)
            choices[b].remove(a)

        mat[c-1][d-1] = week
    # constructing week

    def construct_week(m):

        univ = copy.deepcopy(univ_tab[m-1])
        # n_choices = univ[0]
        # choices = univ[1]
        # all_coors = univ[2]
        # mat = univ[3]
        
        choices_copy = copy.deepcopy(univ[1])

        queue = create_priority_queue(univ[0])

        p_queue = queue[:]
        rest = [i for i in range(1,N+1)]

        while len(p_queue) >=1:

            if len(rest) <= 2:
                if len(rest) == 1:
                    return False
                else:
                    if rest[1] not in univ[1][rest[0]]:
                        return False
                    else:
                        check_choices(choices_copy)
                        choose_match(rest[1], univ[0], univ[1], choices_copy, univ[2], rest, queue, univ[3], m, p_queue, rest[0])
                        return univ
            else:
                check_choices(choices_copy)
                queue = create_priority_queue(create_n_choices(choices_copy))
                p_queue = queue[:]

                i = p_queue[0]

                # print('Week', end ='')
                # print(m)

                choose_match(i, univ[0], univ[1], choices_copy, univ[2], rest, queue, univ[3], m, p_queue)

                if len(choices_copy.keys()) % 2 != 0:
                    return 'Reset'
    try:
        construct_mat(0)
    except Exception:

        construct_mat(0)

    return result


def get_neighbors(initialize): #initialize: mat,cost
    '''return list of (mat,cost)'''
    mat,cost = initialize
    M = copy.deepcopy(mat)
    N = len(M)
    
    all_neighbors = list()

    def team_cost(team,matrix,d_matrix):
        away = list(zip(list(matrix[team][i] for i in range(0,N)),range(1,N+1)))
        home = list(zip(list(matrix[i][team] for i in range(0,N)),list(team + 1 for j in range(0,N))))
        home.sort()
        home.pop(0)
        team_schedule = away + home
        team_schedule.sort()
        C = 0
        for i in range(len(team_schedule)-1):
            C += d_matrix[team_schedule[i][1] - 1][team_schedule[i+1][1] - 1]
        return C
    def match_swap(coor):
        Y = copy.deepcopy(mat)
        temp = Y[coor[0]][coor[1]]
        Y[coor[0]][coor[1]] = Y[coor[1]][coor[0]]
        Y[coor[1]][coor[0]] = temp

        A = team_cost(coor[0],mat,distance_matrix) + team_cost(coor[1],mat,distance_matrix) 
        B = team_cost(coor[0],Y,distance_matrix) + team_cost(coor[1],Y,distance_matrix)
        cost_Y = cost - A + B
        return (Y, cost_Y)

    def team_swap(teams):
        a,b = teams
        a -= 1
        b -= 1
        Y = copy.deepcopy(mat)
        Y_1 = numpy.array(copy.deepcopy(Y))
        
        def replace_in_mat(x,y,S):
            temp = S[x].copy()
            S[x] = S[y].copy()
            S[y] = temp.copy()

            S[x][y] = S[x][x]
            S[x][x] = 0

            S[y][x] = S[y][y]
            S[y][y] = 0

        replace_in_mat(a,b,Y_1)
        Y_1 = Y_1.T.copy()
        
        replace_in_mat(a,b,Y_1)
        Y_1 = Y_1.T.copy()

        Y = copy.deepcopy(Y_1.tolist())
        return (Y, compute_cost(distance_matrix, Y))
    
    iterate = list((j,i) for i in range(0,N) for j in range(0,i))

    for coor in iterate:
        mat_1, cost_1 = copy.deepcopy(match_swap(coor))
        all_neighbors.append((mat_1, cost_1))


    iterate = list((i,j) for i in range(1,N + 1) for j in range(i, N + 1))

    for coor in iterate:
        mat_1, cost_1 = copy.deepcopy(team_swap(coor))
        all_neighbors.append((mat_1, cost_1))
    
    return all_neighbors

def compute_cost(distance_matrix,matrix):
    '''compute cost of a solution'''
    num_of_teams = len(matrix)
    cost = 0
    for team in range(num_of_teams):
        current_pos = team
        team_dis = 0
        current_week = 0
        while current_week < 2*num_of_teams - 2:
            current_week = current_week + 1
            flag = True
            for index in range(num_of_teams):
                if matrix[team][index] == current_week:
                    old_pos = current_pos
                    current_pos = index
                    team_dis += distance_matrix[old_pos][current_pos]
                    flag = False
                    break
            if flag: # da san nha
                old_pos = current_pos
                current_pos = team
                team_dis += distance_matrix[old_pos][current_pos]

        cost += team_dis
        
    return cost       
def local_solve(input):
    # random inial
    #input: distance matrix
    #return the schedule: matrix , cost
    N = len(input)
    random_matrix = generate(N)
    cost = compute_cost(input,random_matrix)
    initialize = random_matrix,cost
    flag = False
    while flag:
        neighbors = get_neighbors(initialize)
        for neighbor in neighbors:
            #neighbor: matrix:schedule,cost
            schedule,cost = neighbor
            flag = False
            if cost < initialize[1]:
                initialize = neighbor
                flag = True
    return initialize[0],initialize[1]

distance_matrix = [[0, 1, 2, 3], [1, 0, 4, 5], [2, 4, 0, 6], [3, 5, 6, 0]]
config_local_search, val_local_search = local_solve(distance_matrix)
print(f'The reasonable cost when using Local Search is {val_local_search}, when: matrix is {config_local_search}')


runtime = time.time() - before
print(f'Runtime: {runtime}')