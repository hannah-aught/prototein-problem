import random
import sys
import math
import re
import time
from Condition import Condition

def read_data(file):
    with open(file, "r") as f:
        data = f.readlines()
        
        return data[0].strip()

def get_positions_of_ones(s):
    positions_of_ones = list()

    for i in range(0, len(s)):
        if s[i] == "1":
            positions_of_ones.append(i)
    
    return positions_of_ones

def get_num_adjacent_ones(positions_of_ones):
    num_adjacent_ones = 0

    for i in range(0, len(positions_of_ones) - 1):
        if abs(positions_of_ones[i] - positions_of_ones[i+1]) == 1:
            num_adjacent_ones += 1
    
    return num_adjacent_ones


def is_binary_string(string):
    for x in string:
        if x != "1" and x != "0":
            return False

    return True

def repeat_count_condition(count_condition, t_ki, t_k, repeats):
    clauses = list(count_condition.clauses)

    for i in range(1, repeats):
        for c in count_condition.clauses:
            new_clause = list()
            last_el = c[len(c) - 1]

            if (len(c) > 1):
                for v in c[:len(c)-1]:
                    if v > 0:
                        v += 2 * i * t_ki
                    else:
                        v -= 2 * i * t_ki
                    new_clause.append(v)

            if last_el > 0:   
                last_el += i * t_k
            else:
                last_el -= i * t_k

            new_clause.append(last_el)
            clauses.append(new_clause)

    count_condition.set_clauses(clauses)

def gen_embedding_conditions(n, grid_width):
    embedding_conditions = list()
    grid_area = pow(grid_width, 2)
    grid_vol = grid_area * grid_width

    # embedding condition 1
    embedding_condition_1 = Condition([range(1, grid_vol + 1)], True, n, grid_vol)
    embedding_conditions.append(embedding_condition_1)

    # embedding condition 2
    embedding_condition_2 = Condition(list(), True, n, grid_vol)

    for i in range(1, grid_vol):
        for j in range(i + 1, grid_vol + 1):
            embedding_condition_2.add_clause([-1 * i, -1 * j])

    embedding_conditions.append(embedding_condition_2)

    # embedding condition 3
    embedding_condition_3 = Condition(list(), True, grid_vol, 1)
    stop = (n - 1) * grid_vol + 1

    for j in range(1, stop, grid_vol):
        for i in range(j+grid_vol, stop+1, grid_vol):
            embedding_condition_3.add_clause([-1 * j, -1 * i])
    
    embedding_conditions.append(embedding_condition_3)

    # embedding condition 4
    embedding_condition_4 = Condition(list(), True, n - 1, grid_vol)

    for j in range(1, grid_vol + 1):
        clause = list()
        clause.append(-1 * j)

        if j % grid_width != 0:
            clause.append(j + grid_vol + 1)
        if j % grid_width != 1:
            clause.append(j + grid_vol - 1)
        if (j % grid_area <= grid_area - grid_width) and j % grid_area != 0:
            clause.append(j + grid_vol + grid_width)
        if j % grid_area > grid_width or j % grid_area == 0:
            clause.append(j + grid_vol - grid_width)
        if j <= (grid_width - 1) * grid_area:
            clause.append(j + grid_vol + grid_area)
        if j > grid_area:
            clause.append(j + grid_vol - grid_area)
        
        embedding_condition_4.add_clause(clause)
    
    embedding_conditions.append(embedding_condition_4)

    return embedding_conditions

def gen_contact_conditions(n, grid_width, positions_of_ones):
    grid_area = pow(grid_width, 2)
    grid_vol = pow(grid_width, 3)
    offset = grid_vol * n #existing vars from X_ij conditions
    contact_conditions = list()
    
    # contact condition 1
    contact_condition_1 = Condition(list(), True, grid_vol, 1)    
    
    for x in positions_of_ones:
        contact_condition_1.add_clause([offset + 1, -1 * (x * grid_vol + 1)])

    last_clause = [-1 * (offset + 1)]
    last_clause.extend(map(lambda x: (x * grid_vol) + 1, positions_of_ones))
    contact_condition_1.add_clause(last_clause)
    contact_conditions.append(contact_condition_1)

    # contact condition 2
    clauses = list()

    for j in range(1, grid_vol + 1):
        C_jr = offset + grid_vol + j
        C_jd = C_jr + grid_vol
        C_jb = C_jd + grid_vol
        T_j = C_jr - grid_vol
        T_jr = T_j + 1
        T_jd = T_j + grid_width
        T_jb = T_j + grid_area

        if j % grid_width != 0:
            clauses.extend([[-1 * C_jr, T_j], [-1 * C_jr, T_jr], [C_jr, -1 * T_j, -1 * T_jr]])
        else:
            clauses.extend([[-1 * C_jr]])
        if j % grid_area <= grid_area - grid_width and j % grid_area > 0:
            clauses.extend([[-1 * C_jd, T_j], [-1 * C_jd, T_jd], [C_jd, -1 * T_j, -1 * T_jd]]) 
        else:
            clauses.extend([[-1 * C_jd]])
        if j <= (grid_width - 1) * grid_area:
            clauses.extend([[-1 * C_jb, T_j], [-1 * C_jb, T_jb], [C_jb, -1 * T_j, -1 * T_jb]])
        else:
            clauses.extend([[-1 * C_jb]])

    contact_condition_2 = Condition(clauses)
    contact_conditions.append(contact_condition_2)

    return contact_conditions

def gen_counting_conditions(n, grid_width, r):
    grid_vol = pow(grid_width, 3)
    num_contact_condition_vars = 3 * grid_vol
    num_tree_levels = math.ceil(math.log(num_contact_condition_vars, 2))
    counting_conditions = list()
    num_existing_vars = grid_vol * n + grid_vol + num_contact_condition_vars
    num_vars = num_existing_vars

    for l in range(1, num_tree_levels - 1):
        t_k = min(r, pow(2, num_tree_levels - l))
        t_ki = min(r, pow(2, num_tree_levels - l - 1))
        repeats = pow(2, l)

        if l < num_tree_levels - 1 and t_k == 2 * t_ki:
            count_condition_l = Condition(list(), True, repeats, t_k)
        else:
            count_condition_l = Condition(list(), False)

        # i and j are the two children of node k.
        for j in range(0, t_ki + 1):
            if l == num_tree_levels - 1:
                b_j_2k =  -1 * (grid_vol * n + grid_vol + t_ki + j)
            else:
                b_j_2k = num_vars + repeats * t_k + t_ki + j # var number will be the existing number of variables + the number of variables at level k + i

            for i in range(0, t_ki + 1):
                clause = list()

                if (i + j) > (t_k + 1):
                    break
                elif i + j < 1:
                    continue

                if l == num_tree_levels - 1:
                    b_i_2k = -1 * (grid_vol * n + grid_vol + i)
                else:
                    b_i_2k = num_vars + repeats * t_k + i # vars number is the existing vars + the number of variables at level k + the number of variables under node i + j

                if not(i == 0):
                    clause.append(-1 * b_i_2k)

                if not(j == 0):   
                    clause.append(-1 * b_j_2k)
                if (i > 0 or j > 0) and i + j < t_k + 1:
                    b_r_k = num_vars + i + j # existing vars + whatever k value we're on (k is the highest node in question for all clauses)
                    clause.append(b_r_k)

                if clause not in count_condition_l.clauses:
                    count_condition_l.add_clause(clause)

        if l < num_tree_levels - 1:
            num_vars += t_k * repeats

        if t_k != 2 * t_ki:
            repeat_count_condition(count_condition_l, t_ki, t_k, repeats)
        counting_conditions.append(count_condition_l)
        

    # TODO: The number of counting variables isn't guaranteed to be even in 3D
    last_level_condition = Condition(list(), False)
    t_k = min(r, 2) # only two nodes below each node on the second to last level
    repeats = pow(2, num_tree_levels - 1)

    for k in range(0, repeats):
        for j in range(0, 2): #only two leaves per pre-terminal node
            for i in range(0, 2):
                last_level_clause = list()
                b_i_2k = -1 * (grid_vol * n + grid_vol + k * t_k + 1)
                b_j_2k = b_i_2k - 1
                b_r_k = num_vars + k * t_k + i + j

                if i + j > t_k + 1:
                    break
                if i + j == 0:
                    continue

                if (b_i_2k < -1 * num_existing_vars or b_j_2k < -1 * num_existing_vars) and i + j == 2:
                    last_level_clause.append(-1 * b_r_k)
                    if last_level_clause not in last_level_condition.clauses:
                        last_level_condition.add_clause(last_level_clause)
                    continue
                elif b_i_2k < -1 * num_existing_vars and b_j_2k < -1 * num_existing_vars:
                    last_level_clause.append(-1 * b_r_k)
                elif b_i_2k < -1 * num_existing_vars and i == 1:
                    continue
                elif b_j_2k < -1 * num_existing_vars and j == 1:
                    continue
                else:
                    last_level_clause.append(b_r_k)

                if i > 0 and b_i_2k >= -1 * num_existing_vars:
                    last_level_clause.append(-1 * b_i_2k)
                if j > 0 and b_j_2k >= -1 * num_existing_vars:
                    last_level_clause.append(-1 * b_j_2k)
                
                if len(last_level_clause) > 0 and last_level_clause not in last_level_condition.clauses:
                    last_level_condition.add_clause(last_level_clause)
    
    counting_conditions.append(last_level_condition)
    num_vars += t_k *repeats
    t_2 = min(r, pow(2, num_tree_levels - 1)) # node 2 is at level 1
    count_condition_2 = Condition(list(), False)

    # there's another way to do this beside doing two nested loops, but is it better?
    for i in range(1, t_2 + 1):
        for j in range(1, t_2 + 1):
            count_clause = list()
            if i + j < r + 1:
                continue
            elif i + j > r + 1:
                break
            if i != 0:
                count_clause.append(-1 * (num_existing_vars + i))
            if j != 0:
                count_clause.append(-1 * (num_existing_vars + t_2 + j))
            if len(count_clause) > 0:
                count_condition_2.add_clause(count_clause)
            
    counting_conditions.append(count_condition_2)

    return list([counting_conditions, num_vars])

def get_num_clauses(n, conditions):
    num_clauses = 0
    #n +  pow(n, 3) * (pow(n, 2) - 1)//2 +  pow(n, 3) * (n - 1)//2 + pow(n, 2) * (n - 1) + pow(n, 2) * (num_existing_ones + 1)

    for i in range(0, len(conditions)):
        num_clauses += conditions[i].num_repeats * len(conditions[i].clauses)

    return num_clauses

def write_conditions(num_vars, num_clauses, conditions, file):
    with open(file, "w") as f:
        print("c " + file, file=f)
        print("c", file=f)
        print("p cnf " + str(num_vars) + " " + str(num_clauses), file=f)
        for c in conditions:
            c.write_condition(f)

def gen_cnf_file(string, grid_width, k, embedding_conditions, contact_conditions, outfile):
    n = len(string)
    grid_vol = grid_width**3
    positions_of_ones = get_positions_of_ones(string)
    num_adjacent_ones = get_num_adjacent_ones(positions_of_ones)
    r = 3 * grid_vol - (num_adjacent_ones + k)
    counting_conditions_num_vars = gen_counting_conditions(n, grid_width, r)
    counting_conditions = counting_conditions_num_vars[0]
    num_vars = counting_conditions_num_vars[1]
    conditions = embedding_conditions + contact_conditions + counting_conditions
    num_clauses = get_num_clauses(n, conditions)
    write_conditions(num_vars, num_clauses, conditions, outfile)

def main(argv):
    if len(argv) <= 3 or len(argv) > 4:
        print("ERROR: wrong number of arguments given\n\tUsage: main.py {input file} {goal number of contacts} {optional output directory}")
        return
    elif len(argv) == 4:
        outdir = argv[3]
    else:
        outdir = "."

    file_name = argv[1]

    string = read_data("./input/" + file_name)

    if not is_binary_string(string):
        print("Error:", string, "is not a binary string")
        return 1

    n = len(string)

    if n >= 20:
        grid_width = 2 + n//8
    else:
        grid_width = 2 + n//4

    outfile = outdir + "/" + file_name + ".cnf"
    positions_of_ones = get_positions_of_ones(string)
    num_adjacent_ones = get_num_adjacent_ones(positions_of_ones)
    k = int(argv[2]) # start by looking for only one contact
    r = 3 * (grid_width ** 3) - (num_adjacent_ones + k)
    embedding_conditions = gen_embedding_conditions(n, grid_width)
    contact_conditions = gen_contact_conditions(n, grid_width, positions_of_ones)
    counting_conditions_num_vars = gen_counting_conditions(n, grid_width, r)
    counting_conditions = counting_conditions_num_vars[0]
    num_vars = counting_conditions_num_vars[1]
    conditions = embedding_conditions + contact_conditions + counting_conditions
    num_clauses = get_num_clauses(n, conditions)
    print("string:", string)
    print("length:", n)
    print("grid diameter:", grid_width)
    print("goal contacts:", k)
    print("using r =", r)
    write_conditions(num_vars, num_clauses, conditions, outfile)
    print("cnf file for", file_name, "written to", outfile)

    return 0

main(sys.argv)
#main(["HPsat-3D.py", "1f8vF0", "10", "./test_output"])