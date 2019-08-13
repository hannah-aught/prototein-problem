from Condition import Condition

def convert(file, offset):
    with open(file, "r") as f:
        line_condition = Condition()
        lines = f.readlines()
        for i, line in enumerate(lines):
            if (i < 3):
                continue
            line = line.strip().split(" ")
            clause = list()
            for val in line:
                if (int(val) < 0):
                    val = int(val) - offset
                elif int(val) > 0:
                    val = int(val) + offset
                else:
                    break
                clause.append(val)
            line_condition.add_clause(clause)

    with open(file, "w+") as newf:
        line_condition.write_condition(newf)
                
convert("./lingeling/input/level6.cnf", 756)