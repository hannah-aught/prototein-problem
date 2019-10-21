import sys
from pathlib import Path
import os
import subprocess

def main(argv):
    input_dir = Path(argv[1])
    result_file_dir = argv[2]

    for x in os.listdir(input_dir):
        with open(input_dir / Path(x), "r") as f:
            dash_index = len(x) - 8
            file_name = x[0:dash_index]

            with open("input/" + file_name, "r") as input_f:
                sequence = input_f.readlines()[0].strip()
                n = len(sequence)

            process_name = "HPb1.pl"

            if n < 12:
                process_name = "HPb.pl"

            subprocess.run(["perl", process_name, "input/" + file_name])
            subprocess.run(["mv", "./input/" + file_name + ".lp", result_file_dir + "/"])

    return

main(["gen_lp_files.py", "2D_output", "2D_lp_files"])# sys.argv)