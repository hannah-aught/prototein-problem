import sys
from pathlib import Path
import os

def is_clause(el):
    return (el[0].isnumeric() or el[1].isnumeric()) and el[0] != "0"

def is_p_line(el):
    return el[0] == "p"

def get_clauses(file_data):
    clauses = filter(is_clause, file_data)
    
    return clauses

def get_num_literals(clauses):
    count = 0

    for clause in clauses:
        clause = clause.split(" ")

    # len(x) - 1 because there is always a tailing 0
    count = sum(len(x) - 1 for x in clauses)

    return count

def get_num_variables(file_data):
    
    p_line = list(filter(is_p_line, file_data))[0]
    p_info = p_line.split(" ")
    num_vars = p_info[2]
    
    return num_vars

def main(argv):
    input_directory = Path(argv[1])
    output_file = argv[2]

    directory_contents = os.listdir(input_directory)

    with open(output_file, "w+") as out:

        for x in directory_contents:
            with open(input_directory / Path(x), "r") as f:
                file_data = f.readlines()
                clauses = list(get_clauses(file_data))
                num_clauses = len(clauses)
                num_literals = get_num_literals(clauses)
                num_vars = get_num_variables(file_data)
                print("\nfilename:", x, "\n  Number of clauses:", num_clauses, "\n  Number of literals:", num_literals,
                "\n  Number of variables:", num_vars, file = out)
    return

main(["get_sat_file_data.py", "3D_sat_files", "3D_sat_data.txt"])#sys.argv)






