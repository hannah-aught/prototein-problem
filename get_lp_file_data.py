import sys
from pathlib import Path
import os

def is_inequality(el):
    return "=" in el or "<" in el or ">" in el

def remove_operators(el):
    return el != "=" and el != "<" and el != ">" and el != "+" and el != "-" and el != ""

def get_inequalities(file_data):
    inequalities = filter(is_inequality, file_data[5:])

    return list(inequalities)

def get_num_literals(inequalities):
    count = 0

    for x in inequalities:
        left_side = x[:len(x) - 3].strip()
        x = list(filter(remove_operators, left_side.split(" ")))
        count = count + len(x)
    
    return count
        
def get_num_variables(inequalities):
    vars_seen = list()
    
    for x in inequalities:
        left_side = x[:len(x) - 3].strip()
        x = list(filter(remove_operators, left_side.split(" ")))
        
        for literal in x:
            if literal not in vars_seen:
                vars_seen.append(literal)
    
    return len(vars_seen)


def main(argv):
    input_directory = Path(argv[1])
    output_file = argv[2]

    directory_contents = os.listdir(input_directory)

    with open(output_file, "w+") as out:

        for x in directory_contents:
            with open(input_directory / Path(x), "r") as f:
                file_data = f.readlines()
                inequalities = list(get_inequalities(file_data))
                num_inequalities = len(inequalities)
                num_literals = get_num_literals(inequalities)
                num_vars = get_num_variables(inequalities)
                print("\nfilename:", x, "\n  Number of inequalities:", num_inequalities, "\n  Number of literals:", num_literals,
                "\n  Number of variables: ", num_vars, file = out)
    return

main(["get_lp_file_data.py", "2D_lp_files", "2D_lp_data.txt"])#sys.argv)