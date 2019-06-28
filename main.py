import random
import sys
from functools import reduce
from Condition import Condition

def nCr(n, r): # Source: https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function - in - python
    r = min(r, n - r)
    mult = lambda x, y: x*y
    numerator = reduce(mult, range(n, n - r, -1), 1)
    denominator = reduce(mult, range(1, r + 1), 1)

    return numerator // denominator

def getPositionsOfOnes(s):
    positionsOfOnes = list()

    for i in range(0, len(s)):
        if s[i] == "1":
            positionsOfOnes.append(i)
    
    return positionsOfOnes

def isBinaryString(string):
    for x in string:
        if x != "1" and x != "0":
            return False

    return True

#n is the length for the binary string that will be produced
def genTestStr(n):
    if n <= 0 or n == None:
        raise Exception("String length must be > 0. Please try again")
    else:
        testStr = str()
        while len(testStr) < n:
            testStr += str(random.randint(0, 1))

        return testStr

#str is the binary string, k is the goal number of contacts
def generateClauses(string, k, positionsOfOnes):
    if not isBinaryString(string):        
        raise Exception("{string} is not a valid binary string")

    n = len(string)
    conditions = list()

    # embedding condition 1 (every x_ij is somewhere)
    clause1 = list()

    for x in range(1, n * n + 1):
        clause1.append(x)

    embedCondition1 = Condition([clause1], True, n, n * n)
    conditions.append(embedCondition1)

    # embedding condition 2 (every x_ij can only be true for one j)
    embedCondition2 = Condition(list(), True, n, n * n)

    for i in range(1, n * n):
        for j in range (i+1, n * n + 1):
            embedCondition2.addClause([-1 * i,-1 * j])
    
    conditions.append(embedCondition2)

    # embedding condition 3 (every x_ij can only be true for one i)
    embedCondition3 = Condition(list(), True, n * n, 1)

    stop = (n - 1) * n * n + 1

    for j in range(1, stop, n * n):
        for i in range(j+n * n, stop+1, n * n):
            embedCondition3.addClause([-1 * j, -1 * i])
    
    conditions.append(embedCondition3)

    # embedding condition 4
    embedCondition4 = Condition(list(), True, n - 1, n * n)
    
    for i in range(1, n * n + 1):
        if i == 1:
            # condition 4f
            embedCondition4.addClause([-1 * i, i + n * n + 1, i + n * n + n])
        elif i == n:
            # conditin 4g
            embedCondition4.addClause([-1 * i, i + n * n - 1, i + n * n + n])
        elif i == n * n - n + 1:
            # condition 4h
            embedCondition4.addClause([-1 * i, i + n * n + 1, i + n * n - n])
        elif i == n * n:
            # condition 4i
            embedCondition4.addClause([-1 * i, i + n * n - 1, i + n * n - n])
        elif i % n == 1:
            # condition 4d
            embedCondition4.addClause([-1 * i, i + n * n + 1, i + n * n + n, i + n * n - n])
        elif i % n == 0:
            # condition 4e
            embedCondition4.addClause([-1 * i, i + n * n - 1, i + n * n + n, i + n * n - n])
        elif i > 1 and i < n:
            # condition 4b
            embedCondition4.addClause([-1 * i, i + n * n + 1, i + n * n - 1, i + n * n + n])
        elif i > n * n - n + 1 and i < n * n:
            # condition 4c
            embedCondition4.addClause([-1 * i, i + n * n + 1, i + n * n - 1, i + n * n - n])
        else:
            embedCondition4.addClause([-1 * i, i + n * n + 1, i + n * n - 1, i + n * n + n, i + n * n - n])

    conditions.append(embedCondition4)

    # contact condition 1
    contactCondition1 = Condition(list(), True, n * n, 1)

    for x in positionsOfOnes:
        contactCondition1.addClause([n * n * n + 1, (-1 * x * n * n) - 1])

    lastClause = [-1 * n * n * n - 1]
    lastClause.extend(map(lambda x: (x * n * n) + 1, positionsOfOnes))
    contactCondition1.addClause(lastClause)

    conditions.append(contactCondition1)

    # contact condition 2
    clauses = list()

    for j in range(1, n * n + 1):
        C_jr = n * n * n + n * n + j
        C_jd = C_jr + n * n
        T_j = C_jr - n * n
        T_jr = T_j + 1
        T_jd = T_j + n

        if j == n * n:
            clauses.extend([[-1 * C_jr]])
            clauses.extend([[-1 * C_jd]])
        elif j >= n * n - n + 1:
            clauses.extend([[-1 * C_jr, T_j], [-1 * C_jr, T_jr], [C_jr, -1 * T_j, -1 * T_jr]])
            clauses.extend([[-1 * C_jd]])
        elif j % n == 0:
            clauses.extend([[-1 * C_jr]])
            clauses.extend([[-1 * C_jd, T_j], [-1 * C_jd, T_jd], [C_jd, -1 * T_j, -1 * T_jd]]) 
        else:
            clauses.extend([[-1 * C_jr, T_j], [-1 * C_jr, T_jr], [C_jr, -1 * T_j, -1 * T_jr]])
            clauses.extend([[-1 * C_jd, T_j], [-1 * C_jd, T_jd], [C_jd, -1 * T_j, -1 * T_jd]])      
    contactCondition2 = Condition(clauses)

    conditions.append(contactCondition2)

    return conditions

def printClauses(clauseArray):
    for x in clauseArray:
        print(x)

def main(argv):
    flag = str()

    if len(argv) < 4 or len(argv) > 5:
        print("ERROR: wrong number of arguments.\n\tUsage: main.py {outfile } {string or length} {goal # of contacts} {-s, -l}")
        print("-s for passing a string, -l for a length, -a for an array")
        return
    else:
        outfile = "../Research/Input/" + argv[1]
        s = argv[2]
        k = int(argv[3])
        flag = argv[4] if len(argv) == 5 else "-l"

        if flag == "-l":
            n = int(s)

            try:
                testStr = genTestStr(int(s))
            except Exception as e:
                print(e)
        elif flag == "-s":
            #we were given a binary string
            n = len(s)
            testStr = s
        else:
            print("ERROR: unknown flag.\n\tUsage: main.py {outFile } {string or length} {goal # of contacts} {-s, -l}")
            print("-s for passing a string, -l for a length")
            return

        positionsOfOnes = getPositionsOfOnes(testStr)
        numExistingOnes = len(positionsOfOnes)
        r = numExistingOnes + k
        conditions = generateClauses(testStr, r, positionsOfOnes)
        numContactCondition2Clauses = len(conditions[5].clauses)
        numVars = n * n * n + 3 * n * n
        numClauses = n + n * n * n * (n * n - 1)//2 + n * n * n * (n - 1)//2 + n * n * (n - 1) + n * n * (numExistingOnes + 1) + numContactCondition2Clauses

        with open(outfile, "w") as f:
            print("c " + outfile + ".cnf\nc\np cnf " + str(numVars) + " " + str(numClauses), file=f)

            for x in conditions:
                x.writeCondition(f)


        return conditions


main(sys.argv) # ["main.py", "test.txt", "11", "2", "-s"])

# TODO: Change contact loop. shouldn't check for contacts on all sides, only one horizontal and one vertical. This will prevent overcounting