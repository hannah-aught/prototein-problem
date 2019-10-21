from enum import Enum


""" 
Hannah Brown, 10/20/19
 * A Condition represents a set of clauses representing one idea that may need
 * to be repeated for many different variables (for example, across all 
 * characters in a string)
 * The num_repeats option and increment option in the class provide a way to
 * describe this repition without having to construct all the clauses and  hold
 * them in memory (it takes a lot of memory)
"""
class Condition:
    clauses = list() # this should now be a list of numbers to allow for easier printing
    repeat = False # Whether these clauses repeat or not
    num_repeats = 1 # num_repeats = 1 means the condition doesn't repeat
    increment = 0 # What to add to each variable when the clauses are repeated

    def __init__(self, clauses = list(), repeat = False,  num_repeats = 1, increment = 0):
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
        # print the condition to a file w/ proper repeats
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