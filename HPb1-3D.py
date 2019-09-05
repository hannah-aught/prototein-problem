# Jonathan Kim
# Project HPb1-3D.py
# Extending 2D ILP generator to handle 3D cases for the HP model of protein folding.
# DG modified July 16, 2019
#
# DG: The name of this program was changed from HPb1_3D.py to HPb1-3D.py, because of typesetting problems in the book, caused by
# having and underscore in the name.
#
# DG: In 3-D we have to be more careful of what we pick for the denominator, where n/denominator =  the width =  length = height of
# the cube. The reason is the value of width such that width**3 = n is smaller than the value of width such that
# width**2 = n. So, even when we set the width to some multiple of the cube root of n (in the 3-D) case, 
# we might create a cube that has sufficient volume to embed the string of length n, 
# but not sufficient width for an optimal embedding.
#
# December 14, 2017
# This runs with Python 2.7
#
# call this program on a command line in a terminal window as:
# python HPb1-3D.py data-file-name ilpfile-name
import sys
import math


arg1 = sys.argv[1]
arg2 = sys.argv[2]

INFILE = open(arg1, "r")  # open the file specified by the value of arg1, to read from the file.
OUT = open(arg2, "w")     # open the file specified by the value of arg2, to write to the file.

sequence = ""
constraints = "\n"  # assign the string `such that \n\n' to the variable `constraints'
objective = ""
Econstraints = ""
binaries = "binary \n"

for sequence in INFILE:
    sequence = sequence.rstrip()

n = len(sequence)
print('%s, %d' % (sequence,n))
if(n >= 20):
    denominator = 8
else:
    denominator = 4
#diam = 4  # DG making the diam as small as possible has a huge effect on the ILP solving time. In the practical use of the ILP approach
           # it might be usefull to do executions where the diam is started small and then extended a little bit at a time to see the
           # effect
diam = 2 + int(n/denominator)   # DG changed 1 to 2 to see if the cube is too small
#diam = 3 + int(n/denominator)   # DG changed 2 to 3 to see if the cube is too small

print('diameter %d' % (diam))
diamsquared = diam**2
diamcubic = diam**3


# loop through the edges in the diam-by-diam grid to set up
# the objective function, and also set up the inequalities to count 
# the number of edges whose endpoints are both assigned a character whose
# value is 1.

k = 1
kp1 = 0

for z  in range(1, diam+1):
    for i  in range(1, diam+1):
        for j  in range(1, diam+1):
            if j < diam:
                kp1 = k + 1 # horizontal edges
                objective = objective + "+ C"+ str(k) + "," + str(kp1) + " "
                Econstraints = Econstraints + "I" + str(k) + " + I" + str(kp1) + " - 2 C" + str(k) + "," + str(kp1) + " >= 0\n"  # C can be set to 1 only if both endpoints are assigned 1s. 
                binaries = binaries + "C" + str(k) + "," + str(kp1) + "\n"

            if i < diam:
                kpn = k + diam # vertical edges
                objective = objective + "+ C" + str(k) + "," + str(kpn) + " "
                Econstraints = Econstraints + "I" + str(k) + " + I" + str(kpn) + " - 2 C" + str(k) + "," + str(kpn) + " >= 0\n"
                binaries = binaries + "C" + str(k) + "," + str(kpn) + "\n"

            if z < diam:
                kpz = k + diamsquared # z edges
                objective = objective + "+ C" + str(k) + "," + str(kpz) + " "
                Econstraints = Econstraints + "I" + str(k) + " + I" + str(kpz) + " - 2 C" + str(k) + "," + str(kpz) + " >= 0\n"
                binaries = binaries + "C" + str(k) + "," + str(kpz) + "\n"

            k += 1
    print('z: %d k: %d' % (z,k-1))
    #k += 1   # increment k to account for the last node in each row.

# HB modified midpoint calculation below 8/29 
midpoint = math.ceil(diam/2) * diamsquared - (diam//2 - 1) * (diam + 1)  # DG added July 13, 2019 in order to try to speed up the ILP

# DG, July 2019. Actually the first position of the string should go in the center of the cube only if that position is an H (hydrophobic).
# Also, in looking at the 3-D solutions in Backhoffen's HPstruck, the first point is rarely in the center, so it is
# worth trying both approaches.

print("midpoint = %d \n" % midpoint)
midpoint2 = midpoint - diamsquared 
#constraints += "X1," + str(midpoint) + " = 1 \n"       # DG July 13, 2019
#constraints += "X2," + str(midpoint2) + " = 1 \n"       # DG July 13

for i in range(1, n+1):   # set up inequalities to ensure each character is assigned to one position
    for pos in range(1, diamcubic+1):
        constraints = constraints + "+ X" + str(i) + "," + str(pos) + " "
        binaries = binaries + "X" + str(i) + "," + str(pos) + "\n"


    constraints = constraints + "=  1 \n"


for pos in range(1, diamcubic+1):   # set up inequalties to ensure each position is assigned at most one character
    for i in range (1, n+1):
        constraints = constraints + "+ X" + str(i) + "," + str(pos) + " "

    constraints = constraints + "<= 1 \n"


# create inequalities to ensure that chars i and i+1 are neighbors on the grid
# first take care of the general cases, and then do the external rows and columns.  

# DG code below is modified July 16, 2019
gridbase = diamsquared + diam + 2 # second plane's second row's second point

for plane in range(2, diam):       # middle planes
    for row in range(2, diam):     # middle rows of middle planes 
        for offset in range(0, diam-2):
            point = gridbase + offset
            for i  in range(1, n):       # each char position i in sequence
                ip1 = i + 1               # the next char poistion
                pointp1 = point + 1          # right point
                pointn1 = point - 1          # left point
                pointpn = point + diam       # down point
                pointnn = point - diam       # up point
                pointpz = point + diamsquared # back point
                pointzz = point - diamsquared # front point


                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0 \n" 
        #constraints = constraints + "end of middle rows and first plane\n"        
        gridbase += diam
#        OUT.write ("After row: the gridbase is now %d \n" % gridbase)
#    gridbase += diamsquared   # DG July 13. I think this is wrong
# HB August 27. Needs to be (plane - 1) rather than (plane)
    gridbase = plane * diamsquared + diam + 2    # DG July 13
#    OUT.write ("After plane: the gridbase is now %d \n" % gridbase)


gridbase = diam + 2     # first plane's second row's second point

for row in range(2, diam):     # middle rows of first plane
    for offset in range(0, diam-2):
        point = gridbase + offset
        for i  in range(1, n):       # each char position i in sequence
            ip1 = i + 1               # the next char poistion
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point


            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz)+ " <= 0\n"
    #constraints = constraints + "end of middle rows and first plane\n"        
    gridbase += diam


gridbase = diamsquared * (diam - 1) + diam + 2    # last plane's second row's second point

for row in range(2, diam):     # middle rows of last plane
    for offset in range(0, diam-2):
        point = gridbase + offset
        for i  in range(1, n):       # each char position i in sequence
            ip1 = i + 1               # the next char poistion
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point


            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz)+ " <= 0\n"
    #constraints = constraints + "end of middle rows of last plane\n"        
    gridbase += diam


#---------------------------------------

# middle planes' first rows, last rows case without corners

gridbase = diamsquared + 2
for plane in range(2, diam):       # middle planes
    for offset in range(0, diam-2):# take care of the middle plane's first rows of the grid, minus the points in the
                                    # first and last columns.
        point = gridbase + offset
        for i in range(1, n):
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES1.1\n")
    gridbase += diamsquared 
        #constraints = constraints + "end of first rows\n"


gridbase = diam * (diam - 1) + diamsquared + 2
for plane in range(2, diam):       # middle planes
    for offset in range(0, diam-2):# take care of the middle plane's last rows of the grid, minus the points in the
                                    # first and last columns.
        point = gridbase + offset
        for i in range(1, n):
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES1.2\n")
    gridbase += diamsquared 
        #constraints = constraints + "end of last rows\n"


#---------------------------------------

# middle planes' first cols, last cols case without corners 

gridbase = diamsquared + diam + 1
for plane in range(2, diam):       # middle planes
    for offset in range(0, diam-2):# take care of the middle plane's first colds of the grid, minus the points in the
                                    # first and last columns.
        point = gridbase + offset * diam
        for i in range(1, n):
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES1.1\n")
    gridbase += diamsquared 
        #constraints = constraints + "end of first rows\n"


gridbase = diamsquared + (diam*2)
for plane in range(2, diam):       # middle planes
    for offset in range(0, diam-2):# take care of the middle plane's last cols of the grid, minus the points in the
                                    # first and last rowss.
        point = gridbase + offset * diam
        for i in range(1, n):
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

            if pointn1 < 0:
                print("YIKES1.2\n")
    gridbase += diamsquared 
       # constraints = constraints + "end of last rows\n"

#--------------------------------------------

# fisrt plane's row, col case without corners

gridbase = 2
for offset in range(0, diam-2):# take care of the fisrt plane's first row of the grid, minus the points in the
                                # first and last columns.
    point = gridbase + offset
    for i in range(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES1\n")
    #constraints = constraints + "end of first rows\n" 


gridbase = diam * (diam - 1) + 2
for offset in range(0, diam-2):# take care of the first plane's last row of the grid, minus the points in the
                                # first and last columns.
    point = gridbase + offset
    for i in range(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES2\n")


gridbase = diam  + 1
for offset in range (0, diam-2): # take care of the first plane's first column minus the corners.
    point = gridbase + offset * diam
    for i  in range (1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES3")


gridbase = 2*diam
for offset in range(0, diam-2): # take care of the first planes' last column minus the corners.
    point = gridbase + offset * diam
    for i in range(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES4")
            #print("$i, $ip1, $gridbase, $offset, $point, $pointn1, $pointpn, $pointnn \n")
            print('%d, %d, %d, %d, %d, %d, %d, %d' % (i, ip1, gridbase, offset, point, pointn1, pointpn, pointnn))

#--------------------------------------------------------------


# last plane's row, col case without corners

gridbase = diamsquared * (diam - 1) + 2
for offset in range(0, diam-2):# take care of the last plane's first row of the grid, minus the points in the
                                # first and last columns.
    point = gridbase + offset
    for i in range(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES1\n")
    #constraints = constraints + "end of last plane's first rows\n" 


gridbase = (diamsquared * (diam - 1)) + (diam * (diam -1)) + 2
for offset in range(0, diam-2):# take care of the last plane's last row of the grid, minus the points in the
                                # first and last columns.
    point = gridbase + offset
    for i in range(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES2\n")


gridbase = diamsquared * (diam-1) + diam + 1
for offset in range (0, diam-2): # take care of the last plane's first column minus the corners.
    point = gridbase + offset * diam
    for i  in range (1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES3")


gridbase = (diamsquared * (diam-1)) + (diam*2)
for offset in range(0, diam-2): # take care of the last planes' last column minus the corners.
    point = gridbase + offset * diam
    for i in range(1, n):
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

        constraints = constraints + "X" + str(i) + "," + str(point) + " "
        constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

        if pointn1 < 0:
            print("YIKES4")
            print('%d, %d, %d, %d, %d, %d, %d, %d' % (i, ip1, gridbase, offset, point, pointn1, pointpn, pointnn))

#constraints += "Middle corner starts \n"
#--------------------------------------------------------------------

# take care of the middle corners

checker = [diamsquared + 1, diamsquared + diam, diam * (diam-1) + diamsquared + 1, diamsquared + diamsquared]
for plane  in  range(2, diam):
    for i  in range(1, n):
        for point in checker:  # take care of the corner cases
            ip1 = i + 1
            pointp1 = point + 1          # right point
            pointn1 = point - 1          # left point
            pointpn = point + diam       # down point
            pointnn = point - diam       # up point
            pointpz = point + diamsquared # back point
            pointzz = point - diamsquared # front point

              
            if point == checker[0]:
                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

                if pointn1 < 0:
                    print("YIKES5")

            if point == checker[2]:
                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"


            if point == checker[1]:
                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"


            if point == checker[3]:
                constraints = constraints + "X" + str(i) + "," + str(point) + " "
                constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0\n"

                if pointn1 < 0:
                    print("YIKES6")
    checker[0] += diamsquared
    checker[1] += diamsquared
    checker[2] += diamsquared
    checker[3] += diamsquared
    #print("%d %d %d %d" % (checker[0],checker[1],checker[2],checker[3]))

#constraints += "Only corner starts \n"
#------------------------------------------------------

# take care of the corners

# the values in checkers are the positions of the 8 corners of the cube. This initialization seems correct. July 11, 2019
checkers = [1, diam, diam * (diam-1) + 1, diamsquared, diamsquared*(diam-1)+1, diamsquared*(diam-1)+diam, (diamsquared*(diam-1)) + (diam * (diam-1) + 1), diamcubic]

for i  in range(1, n):
    for point in checkers:  # take care of the corner cases
        ip1 = i + 1
        pointp1 = point + 1          # right point
        pointn1 = point - 1          # left point
        pointpn = point + diam       # down point
        pointnn = point - diam       # up point
        pointpz = point + diamsquared # back point
        pointzz = point - diamsquared # front point

          
        if point == 1:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0 \n"
#  bottom plane, top left corner\n"

            if pointn1 < 0:
                print("YIKES5")

        if point == diam * (diam - 1) + 1:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0 \n"
#bottom plane, bottom left corner\n"


        if point == diam:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0 \n"
# bottom plane, top right corner


        if point == diamsquared:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointpz) + " <= 0 \n"
# bottom plane, bottom right corner 

            if pointn1 < 0:
                print("YIKES6")

        if point == checkers[4]:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0 \n"
#top plane, top left 

            if pointn1 < 0:
                print("YIKES5")

        if point == checkers[5]:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "

            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0 \n"
# top plane, top right \n"
#            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0 top plane, top right \n" DG this seem wrong. The fix is above.


        if point == checkers[6]:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "

            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0 \n"
#top plane, bottom left 

#            constraints = constraints + "- X" + str(ip1) + "," + str(pointp1) + " - X" + str(ip1) + "," + str(pointpn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0 top plane, bottom left \n" # DG this seems wrong. The fix is above.


        if point == checkers[7]:
            constraints = constraints + "X" + str(i) + "," + str(point) + " "
            constraints = constraints + "- X" + str(ip1) + "," + str(pointn1) + " - X" + str(ip1) + "," + str(pointnn) + " - X" + str(ip1) + "," + str(pointzz) + " <= 0 \n"
# top plane, bottom right

            if pointn1 < 0:
                print("YIKES6")


# Now we create the inequalities to determine if a point has been assigned a 1 or not. Assign I$i to 1 if and only if
# grid point $i has been assigned a 1

inputs  = list(sequence)
ones = {}
lastchar = 0
neighbors1 = 0

for char in range(0, n):        # use hash %ones to record the positions of the 1s in the sequence, and count
                               # the number of adjacent 1s. The objective function is reduced by that count.        
    print('%d %s' % (char,inputs[char])) 

    if inputs[char] == '1':
        if lastchar == 1:
            neighbors1 += 1   
        ones[char] = 1
        lastchar = 1

    else:
        lastchar = 0

print('Neighbor count: %d ' % neighbors1) 

for pos in range(1, diamcubic+1):
    assigned1 = ""
    for char in sorted(ones.keys()):
        charp1 = char + 1
        assigned1 = assigned1 + "+ X" + str(charp1) + "," + str(pos) + " "

    binaries = binaries + "I" + str(pos) + " \n"
    constraints = constraints + assigned1 + "- I" + str(pos) + " = 0 \n"



INFILE.close()
OUT.write("Maximize \n")  # write to file the string (word) 'Maximize' and move to a new line (because of '\n')
#OUT.write(objective + "- Offset \n\n") #DG change Dec. 16, 2018
OUT.write("S \n") #DG added Dec. 16, 2018
OUT.write("subject to \n")
# OUT.write("S >= 15\n")
OUT.write(objective + "- Offset - S = 0 \n\n") # DG added Dec. 16, 2018
OUT.write("Offset = " + str(neighbors1) + "\n")
OUT.write(constraints + " \n\n")
OUT.write(Econstraints + " \n\n")
OUT.write(binaries + " \n")  # write to file the value of the variable 'binaries'
OUT.write("end")  # write to file the string (word) 'end'
OUT.close()
print ("The ILP file is %s \n" %  arg2)

