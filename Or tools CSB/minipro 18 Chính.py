import random as rd
# Tạo sol trước -> sinh dữ liệu để chắc chắn dữ liệu sinh ra chạy được + khi đó thêm các dữ liệu nhiễu vô -> tạo input hoàn chỉnh
def genData(filename, N, M, M_STUDENTS, MAX_DAY): 
    f = open(filename, "w")
    f.write(str(N) + '\n')
    d = [rd.randint(10, M_STUDENTS) for i in range(N)]
    X = [[0 for slot in range(MAX_DAY * 4)] for r in range(M)]
    # X[r][s] is the index of course assigned to the room r 

    x_slot = [0 for i in range(N)]  
    x_room = [0 for i in range(N)]  
    courses = [i for i in range(N)]
    cap = [i for i in range(N)]

    for s in range(MAX_DAY*4): 
        for r in range(M): 
            if len(courses) > 0: 
                idx = rd.randint(0, len(courses) - 1)
                c = courses[idx]
                courses.remove(c)
                X[r][s] = c
                x_slot[c] = s
                x_room[c] = r
                cap[r] = max(cap[r], d[c])
            else: 
                break 
    
    conflict = []
    for i in range(N): 
        for j in range(i+1, N): 
            if x_slot[i] != x_slot[j]: 
                conflict.append([i, j])

# write to file: 
    f.write(str(N) + '\n')
    for i in range(N): 
        f.write(str(d[i]) + ' ')
    f.write('\n')

    f.write(str(M) + '\n')
    for r in range(M): 
        f.write(str(cap[r]) + ' ')
    f.write('\n')     

    f.write(str(len(conflict)) + '\n') 
    for e in conflict: 
        f.write(str(e[0]) + ' ' + str(e[1]) + '\n')

genData("pro8.txt", 10, 2, 100, 10)  