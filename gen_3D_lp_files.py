import sys
from pathlib import Path
import os
import subprocess

def main(argv):
    input_dir = Path(argv[1])
    result_file_dir = argv[2]

    for x in os.listdir(input_dir):
        with open(input_dir / Path(x), "r") as f:
            dash_index = len(x) - 7
            file_name = "input/" + x[0:dash_index]
            output_file = result_file_dir + "/" + x[0:dash_index] + ".lp"
            subprocess.run(["python3", "HPb1-3D.py", file_name, output_file])

    return

main(sys.argv)