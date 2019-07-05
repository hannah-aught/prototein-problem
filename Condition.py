from enum import Enum

class Condition:
    clauses = list() # this should now be a list of numbers to allow for easier printing
    repeat = False
    num_repeats = 0
    increment = 0

    def __init__(self, clauses = list(), repeat = False,  num_repeats = 0, increment = 0):
        self.clauses = clauses
        self.repeat = repeat
        self.num_repeats = num_repeats
        self.increment = increment

    def set_clauses(self, clauses):
        self.clauses = clauses
    
    def set_repeat(self, repeat):
        self.repeat = repeat

    def set_num_repeats(self, num):
        self.num_repeats = num

    def set_increment(self, increment):
        self.increment = increment
            
    def add_clause(self, clause):
        self.clauses.append(clause)

    def write_condition(self, out_file):
        # print the condition w/ proper repeats
        # Loop over clauses, incrementing w/ first increment
        # then loop over clauses w/ subsequent increments until done

        for x in self.clauses:
            for y in x:
                if y == 0:
                    raise Exception("ERROR: 0 found in a clause")
                print(y, end=" ", file=out_file)
            print("0", file=out_file)

        if self.repeat:
            for x in range(1, self.num_repeats):
                for y in self.clauses:
                    for z in y:               
                        if z < 0:
                            print(str(z - x * self.increment), end=" ", file=out_file)
                        else:
                            print(str(z + x * self.increment), end=" ", file=out_file)

                                            
                    print("0", file=out_file)