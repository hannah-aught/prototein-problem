import sys

def get_amino_acid_sequence(original_sequence):
    ONES = ['A', 'C','G', 'I', 'L', 'M', 'F', 'P', 'W', 'Y', 'V']
    ZEROS = ['R', 'N', 'D', 'Q', 'E', 'H', 'K', 'S', 'T']

    sequence = ""

    for x in original_sequence:
        if x in ONES:
            sequence += "1"
        elif x in ZEROS:
            sequence += "0"
        else:
            raise Exception("ERROR: invalid character in sequence: {x}")

    return sequence

def main(argv):
    if (len(argv) < 2):
        raise Exception("ERROR: Usage\n\tpython3 get_sequences.py {path to file to read from}")
    else:
        file = argv[2]
    with open(file, "r") as f: # don't need to write to file, just read contents
        # parse the remarks and assign original_sequence and coordinates
        file_contents = f.read()
        remarks = file_contents.split("REMARK")
        print(remarks)

main(sys.argv)


"""
A     1
R     0
N     0
D     0
C     1
Q     0
E     0
G     1
H     0
I      1
L     1
K     0
M    1
F     1
P     1
S     0
T     0
W    1
Y     1
V     1
"""
