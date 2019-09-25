import sys
from pathlib import Path
import os
import subprocess

def get_num_contacts(cnf_file_data):
    num_contacts = 0

    for line in cnf_file_data:
        if "contacts" in line:
            end_of_words = line.rfind(":")
            num_contacts = line[end_of_words + 2:len(line) - 1]
            break
    
    return num_contacts

def main(argv):
    input_dir = Path(argv[1])
    result_file_dir = argv[2]

    for x in os.listdir(input_dir):
        with open(input_dir / Path(x), "r") as f:
            file_data = f.readlines()
            dash_index = len(x) - 7
            file_name = x[0:dash_index]
            num_contacts = get_num_contacts(file_data)
            subprocess.run(["python3", "HPsat.py", file_name, num_contacts, result_file_dir])

    return


main(["gen_cnf_files.py", "3D_output", "3D_lp_files"])#sys.argv)