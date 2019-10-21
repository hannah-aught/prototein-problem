import random
import sys

def main(argv):
    length = int(argv[1])
    n = int(argv[2])
    prob = float(argv[3])
    file_path = argv[4]
    file_name_base = file_path + "/" + argv[5] if len(argv) == 6 else file_path + "/length" + str(length)
    a = 0
    b = 1/prob
    strings = list()

    while len(strings) < n:
        next_str = ""

        while len(next_str) < length:
            if random.uniform(a,b) <= 1:
                next_str += "1"
            else:
                next_str += "0"
            
        if next_str not in strings:
            strings.append(next_str)
            file_name = file_name_base + "_" + str(len(strings))

            with open(file_name, "w+") as f:
                print(strings[len(strings) - 1])
                print(strings[len(strings) - 1], file=f)

main(sys.argv)   
#main(["gen_random_sequences.py", "5", "5", ".333", "./output", "test"])