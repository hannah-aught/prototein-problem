import random
import sys
import math
from functools import reduce
from Condition import Condition


# Speedup for optimization. Don't use n^2 grid, use n^2/16 for suitably large proteins
# Speedup for 3d. look at email for size of grid
# Speedup: speedup. Have clause that puts left or right end in center of grid. Possible that it'll result in impossible solution.
# might have to increase grid size if we do this
# Speedup: keep solver from looking @ symmetric solutions. If you put left end in middle, position of second one is equivalent no
# matter where it goes. Set position of 2nd (e.g. set to 1 above/below/left/right)
# Speedup: implement a better bound for k based on string

def nCr(n, r): # Source: https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function - in - python
    r = min(r, n - r)
    mult = lambda x, y: x*y
    numerator = reduce(mult, range(n, n - r, -1), 1)
    denominator = reduce(mult, range(1, r + 1), 1)

    return numerator // denominator

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

#n is the length for the binary string that will be produced
def gen_test_str(n):
    if n <= 0 or n == None:
        raise Exception("String length must be > 0. Please try again")
    else:
        test_str = str()
        while len(test_str) < n:
            test_str += str(random.randint(0, 1))

        return test_str

#str is the binary string, r is the goal number of contacts
def generate_clauses(string, r, positions_of_ones):
    if not is_binary_string(string):        
        raise Exception("{string} is not a valid binary string")

    n = len(string)
    conditions = list()

    # embedding condition 1 (every x_ij is somewhere)
    clause_1 = list()

    for x in range(1, n * n + 1):
        clause_1.append(x)

    embed_condition_1 = Condition([clause_1], True, n, n * n)
    conditions.append(embed_condition_1)

    # embedding condition 2 (every x_ij can only be true for one j)
    embed_condition_2 = Condition(list(), True, n, n * n)

    for i in range(1, n * n):
        for j in range (i+1, n * n + 1):
            embed_condition_2.add_clause([-1 * i,-1 * j])
    
    conditions.append(embed_condition_2)

    # embedding condition 3 (every x_ij can only be true for one i)
    embed_condition_3 = Condition(list(), True, n * n, 1)

    stop = (n - 1) * n * n + 1

    for j in range(1, stop, n * n):
        for i in range(j+n * n, stop+1, n * n):
            embed_condition_3.add_clause([-1 * j, -1 * i])
    
    conditions.append(embed_condition_3)

    # embedding condition 4
    embed_condition_4 = Condition(list(), True, n - 1, n * n)
    
    for i in range(1, n * n + 1):
        if i == 1:
            # condition 4f
            embed_condition_4.add_clause([-1 * i, i + n * n + 1, i + n * n + n])
        elif i == n:
            # conditin 4g
            embed_condition_4.add_clause([-1 * i, i + n * n - 1, i + n * n + n])
        elif i == n * n - n + 1:
            # condition 4h
            embed_condition_4.add_clause([-1 * i, i + n * n + 1, i + n * n - n])
        elif i == n * n:
            # condition 4i
            embed_condition_4.add_clause([-1 * i, i + n * n - 1, i + n * n - n])
        elif i % n == 1:
            # condition 4d
            embed_condition_4.add_clause([-1 * i, i + n * n + 1, i + n * n + n, i + n * n - n])
        elif i % n == 0:
            # condition 4e
            embed_condition_4.add_clause([-1 * i, i + n * n - 1, i + n * n + n, i + n * n - n])
        elif i > 1 and i < n:
            # condition 4b
            embed_condition_4.add_clause([-1 * i, i + n * n + 1, i + n * n - 1, i + n * n + n])
        elif i > n * n - n + 1 and i < n * n:
            # condition 4c
            embed_condition_4.add_clause([-1 * i, i + n * n + 1, i + n * n - 1, i + n * n - n])
        else:
            embed_condition_4.add_clause([-1 * i, i + n * n + 1, i + n * n - 1, i + n * n + n, i + n * n - n])

    conditions.append(embed_condition_4)

    # contact condition 1
    contact_condition_1 = Condition(list(), True, n * n, 1)

    for x in positions_of_ones:
        contact_condition_1.add_clause([n * n * n + 1, (-1 * x * n * n) - 1])

    last_clause = [-1 * n * n * n - 1]
    last_clause.extend(map(lambda x: (x * n * n) + 1, positions_of_ones))
    contact_condition_1.add_clause(last_clause)

    conditions.append(contact_condition_1)

    # contact condition 2
    clauses = list()

    for j in range(1, n * n + 1):
        C_jr = n * n * n + n * n + j
        C_jd = C_jr + n * n
        T_j = C_jr - n * n
        T_jr = T_j + 1
        T_jd = T_j + n

        if j == n * n:
            clauses.extend([[-1 * C_jr]])
            clauses.extend([[-1 * C_jd]])
        elif j >= n * n - n + 1:
            clauses.extend([[-1 * C_jr, T_j], [-1 * C_jr, T_jr], [C_jr, -1 * T_j, -1 * T_jr]])
            clauses.extend([[-1 * C_jd]])
        elif j % n == 0:
            clauses.extend([[-1 * C_jr]])
            clauses.extend([[-1 * C_jd, T_j], [-1 * C_jd, T_jd], [C_jd, -1 * T_j, -1 * T_jd]]) 
        else:
            clauses.extend([[-1 * C_jr, T_j], [-1 * C_jr, T_jr], [C_jr, -1 * T_j, -1 * T_jr]])
            clauses.extend([[-1 * C_jd, T_j], [-1 * C_jd, T_jd], [C_jd, -1 * T_j, -1 * T_jd]])

    contact_condition_2 = Condition(clauses)
    conditions.append(contact_condition_2)


    # counting conditions 1 and 2
    # make one condition per level w/ appropriate # of repeats
    num_tree_levels = 2 * math.ceil(math.log(n, 2)) + 1
    num_vars = n*n*n + 3*n*n

    for l in range(1, num_tree_levels):
        t_k = min(r, pow(2, num_tree_levels - l))
        t_ki = min(r, pow(2, num_tree_levels - l - 1))
        repeats = pow(2, l)
        count_condition_l = Condition(list(), True, repeats, t_k)

        for k in range(1, t_k + 1):
            # i and j are the two children of node k.
            for i in range(1, t_ki + 1):
                if l == num_tree_levels - 1:
                    b_i_2k = n * n * n + n * n + i
                else:
                    b_i_2k = num_vars + repeats * t_k + i  # var number will be the existing number of variables + the number of variables at level k + i

                for j in range(1, t_ki + 1):
                    if (i + j) > (t_ki +  1):
                        break
                    if l == num_tree_levels - 1:
                        b_j_2k = n * n * n + n * n + t_ki + j 
                    else:
                        b_j_2k = num_vars + repeats * t_k + t_ki + j # vars number is the existing vars + the number of variables at level k + the number of variables under node i + j

                    b_rk = num_vars + i + j - 1 # existing vars + whatever k value we're on (k is the highest node in question for all clauses)
                    clause = [b_i_2k, b_j_2k, -1 * b_rk]
                    if clause not in count_condition_l.clauses:
                        count_condition_l.add_clause(clause)

        if l < num_tree_levels - 1:
            num_vars += t_k * repeats
        conditions.append(count_condition_l)

    num_vars += t_k * repeats
    t_2 = min(r, pow(2, num_tree_levels - 1)) # node 2 is at level 1
    existing_vars = n * n * n + 3 * n * n
    count_condition_2 = Condition(list(), False)
    for i in range(1, t_2 + 1):
        j = t_2 + 1 - i
        count_condition_2.add_clause([existing_vars + i, existing_vars + t_2 + j ])

    conditions.append(count_condition_2)

    return list([conditions, num_vars])

def print_clauses(clauseArray):
    for x in clauseArray:
        print(x)

def main(argv):
    flag = str()

    if len(argv) < 4 or len(argv) > 5:
        print("ERROR: wrong number of arguments.\n\tUsage: main.py {outfile } {string or length} {goal # of contacts} {-s, -l}")
        print("-s for passing a string, -l for a length, -a for an array")
        return
    else:
        outfile = "./lingeling/input/" + argv[1]
        s = argv[2]
        k = int(argv[3])
        flag = argv[4] if len(argv) == 5 else "-l"

        if flag == "-l":
            n = int(s)

            try:
                test_str = gen_test_str(int(s))
            except Exception as e:
                print(e)
        elif flag == "-s":
            #we were given a binary string
            n = len(s)
            test_str = s
        else:
            print("ERROR: unknown flag.\n\tUsage: main.py {outFile } {string or length} {goal # of contacts} {-s, -l}")
            print("-s for passing a string, -l for a length")
            return

        positions_of_ones = get_positions_of_ones(test_str)
        num_existing_ones = len(positions_of_ones)
        num_adjacent_ones = get_num_adjacent_ones(positions_of_ones)
        r = num_adjacent_ones + k
        conditions_num_vars = generate_clauses(test_str, r, positions_of_ones)
        conditions = conditions_num_vars[0]
        num_vars = conditions_num_vars[1] # n * n * n + 3 * n * n
        
        numcontact_condition_2_clauses = len(conditions[5].clauses)
        num_counting_condition_clauses = 0
        for i in range(6, len(conditions)):
            num_counting_condition_clauses += conditions[i].num_repeats * len(conditions[i].clauses)

        #TODO: make get_num_clauses function instead
        num_clauses = n + n * n * n * (n * n - 1)//2 + n * n * n * (n - 1)//2 + n * n * (n - 1) + n * n * (num_existing_ones + 1) + numcontact_condition_2_clauses + num_counting_condition_clauses

        with open(outfile, "w") as f:
            print("c " + outfile + ".cnf\nc\np cnf " + str(num_vars) + " " + str(num_clauses), file=f)

            for x in conditions:
                x.write_condition(f)


        return conditions


main(["main.py", "test.txt", "11", "1", "-s"])

# TODO: Change contact loop. shouldn't check for contacts on all sides, only one horizontal and one vertical. This will prevent overcounting