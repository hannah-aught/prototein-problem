import random
import sys
import math
import subprocess
import re
import time
from Condition import Condition

main(sys.argv)

def main(argv):
    if len(argv) <= 2:
        print("ERROR: wrong number of arguments given\n\tUsage: main.py {list of input files} -o {output directory}")
        return
    elif "-o" in argv:
        outdir_index = argv.index("-o") + 1
        outdir = argv[outdir_index]
    else:
        outdir_index = argv.length
        outdir = "./output"
    
    files = argv[1:outdir_index - 1]

    for file_name in files:
        string = read_data("./input/" + file_name)

        if not is_binary_string(string):
            print("Error:", string, " is not a binary string")
            continue

        n = len(string)

        if n >= 12:
            grid_width = 1 + n//4
        else:
            grid_width = n

        k = 1 # start by looking for only one contact
        ling_output_file = "./lingeling/input/" + file_name + ".cnf"
        embedding_conditions = gen_embedding_conditions(n, grid_width)
        positions_of_ones = get_positions_of_ones(string)
        contact_conditions = gen_contact_conditions(n, grid_width, positions_of_ones)
        outfile = outdir + "/" + file_name + "_opt.txt"
        ling_time_elapsed = [0,0]
        gurobi_time_elapsed = [0]

        lingeling_max_contacts = maximize_contacts(string, grid_width, k, embedding_conditions, contact_conditions, ling_output_file, ling_time_elapsed, dict())
        with open(outfile, "a+") as out:
            print("\nMaximum contacts found for", string, "using Lingeling:", lingeling_max_contacts, file=out)
            print("plingeling time taken:", ling_time_elapsed[0], file=out)
            print("plingeling runs required:", ling_time_elapsed[1], file=out)

        gurobi_max_contacts = maximize_with_gurobi(file_name, gurobi_time_elapsed, n)

        with open(outfile, "a+") as out:
            print("Maximum contacts found for", string, "using gurobi:", gurobi_max_contacts, file=out)
            print("Gurobi time taken:", gurobi_time_elapsed[0], file=out)

    return 0

def maximize_with_gurobi(file, time_elapsed, flag):
    sol_file = "./gurobi_output/" + file + ".sol"
    lp_file = "./input/" + file + ".lp"

    if (flag != "-o"):
        subprocess.run(["perl", "./HPb.pl", "./input/" + file])
    else:
        subprocess.run(["perl", "./HPb1.pl", "./input/" + file])

    start = time.time()
    result = subprocess.run(["gurobi_cl", "ResultFile=" + sol_file, lp_file], capture_output=True)
    end = time.time()

    if (result.returncode == 1):
        print(str(result.stdout))
        return
    else:
        with open("./gurobi_output/" + file + ".sol") as f:
            lines = f.readlines()
            if "value =" in lines[0]:
                contacts_found = re.search(r"\d+", lines[0]).group()
            else:
                contacts_found = 0
                
            time_elapsed[0] = end - start
            return contacts_found

def bin_search(string, grid_width, min_k, max_k, embedding_conditions, contact_conditions, outfile, time_elapsed, k_vals_tried = dict()):
    k = math.ceil((min_k + max_k) / 2)

    if k == 0:
        return 0

    if k in k_vals_tried:
        if k_vals_tried[k]:
            if min_k == max_k:
                return k
            return bin_search(string, grid_width, k, max_k, embedding_conditions, contact_conditions, outfile, time_elapsed, k_vals_tried)
        else:
            return bin_search(string, grid_width, min_k, k - 1, embedding_conditions, contact_conditions, outfile, time_elapsed, k_vals_tried)

    else:
        print("Trying with k =", k)
        gen_cnf_file(string, grid_width, k, embedding_conditions, contact_conditions, outfile)
        print("Calling lingeling")
        start = time.time()
        result = subprocess.run(["./lingeling/lingeling", outfile], capture_output=True)
        end = time.time()
        time_elapsed[0] += end - start
        time_elapsed[1] += 1 #another try

        if result.returncode < 10:
            print(result.stderr)
            return 0
        elif result.returncode == 10:
            if (min_k == max_k):
                return k
            k_vals_tried[k] = True
            return bin_search(string, grid_width, k, max_k, embedding_conditions, contact_conditions, outfile, time_elapsed, k_vals_tried)
        elif result.returncode == 20:
            k_vals_tried[k] = False
            return bin_search(string, grid_width, min_k, k-1, embedding_conditions, contact_conditions, outfile, time_elapsed, k_vals_tried)
        else:
            print("I found a bug! Unaccounted for return code: " + result.returncode)
    
def maximize_contacts(string, grid_width, k, embedding_conditions, contact_conditions, outfile, time_elapsed, k_vals_tried=dict()):
    if k == 0:
        return 0

    print("Generating file with k =", k)
    gen_cnf_file(string, grid_width, k, embedding_conditions, contact_conditions, outfile)
    print("File generated")
    start = time.time()
    result = subprocess.run(["./lingeling/lingeling", outfile], capture_output=True)
    end = time.time()
    time_elapsed[0] += end - start
    time_elapsed[1] += 1

    if result.returncode < 10:
        print(result.stderr)
        return
    elif result.returncode == 10:
        k_vals_tried[k] = True
        return maximize_contacts(string, grid_width, 2 * k, embedding_conditions, contact_conditions, outfile, time_elapsed, k_vals_tried)
    elif result.returncode == 20:
        k_vals_tried[k] = False
        return bin_search(string, grid_width, k // 2, k-1, embedding_conditions, contact_conditions, outfile, time_elapsed, k_vals_tried)
    else:
        print("I found a bug! Unaccounted for return code: " + result.returncode)

def gen_cnf_file(string, grid_width, k, embedding_conditions, contact_conditions, outfile):
    n = len(string)
    grid_size = pow(grid_width, 2)
    positions_of_ones = get_positions_of_ones(string)
    num_adjacent_ones = get_num_adjacent_ones(positions_of_ones)
    r = 2 * grid_size - (num_adjacent_ones + k)
    counting_conditions_num_vars = gen_counting_conditions(n, grid_width, r)
    counting_conditions = counting_conditions_num_vars[0]
    num_vars = counting_conditions_num_vars[1]
    conditions = embedding_conditions + contact_conditions + counting_conditions
    num_clauses = get_num_clauses(n, conditions)
    write_conditions(num_vars, num_clauses, conditions, outfile)

def gen_embedding_conditions(n, grid_width):
    embedding_conditions = list()
    grid_area = pow(grid_width, 2)
    grid_vol = grid_area * grid_width

    # embedding condition 1
    embedding_condition_1 = Condition(range(1, grid_vol), True, n, grid_vol)
    embedding_conditions.append(embedding_condition_1)

    # embedding condition 2
    # embedding_condition_2 = Condition(list(), True, )
    return embedding_conditions

def gen_contact_conditions(n, grid_width, positions_of_ones):
    contact_conditions = list()
    return contact_conditions

def gen_counting_conditions(n, grid_width, r):
    counting_conditions = list()
    return counting_conditions

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