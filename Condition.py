from enum import Enum

class Condition:
    clauses = list() # this should now be a list of numbers to allow for easier printing
    repeat = False
    numRepeats = 0
    increment = 0

    def __init__(self, clauses = list(), repeat = False,  numRepeats = 0, increment = 0):
        self.clauses = clauses
        self.repeat = repeat
        self.numRepeats = numRepeats
        self.increment = increment

    def setClauses(self, clauses):
        self.clauses = clauses
    
    def setRepeat(self, repeat):
        self.repeat = repeat

    def setNumRepeats(self, num):
        self.numRepeats = num

    def setIncrement(self, increment):
        self.increment = increment
            
    def addClause(self, clause):
        self.clauses.append(clause)

    def writeCondition(self, outFile):
        # print the condition w/ proper repeats
        # Loop over clauses, incrementing w/ first increment
        # then loop over clauses w/ subsequent increments until done

        for x in self.clauses:
            for y in x:
                if y == 0:
                    raise Exception("ERROR: 0 found in a clause")
                print(y, end=" ", file=outFile)
            print("0", file=outFile)

        if self.repeat:
            for x in range(1, self.numRepeats):
                for y in self.clauses:
                    for z in y:               
                        if z < 0:
                            print(str(z - x * self.increment), end=" ", file=outFile)
                        else:
                            print(str(z + x * self.increment), end=" ", file=outFile)

                                            
                    print("0", file=outFile)