from pysat.solvers import Solver
import math
import time

start = time.time() #start timer

r = 3 #number of colours
n = 3 #minimum value of n

#equation: ax + by = cz

#take constants a, b, and c as input
a = int(input())
b = int(input())
c = int(input())

#return mapped variable (integer from [1, r * n])
#col = colour of variable, pos = position of variable
def mapped_variable(col, pos):
    return (pos - 1) * r + col

#return colour of variable (integer from [1, r])
#var = mapped variable
def variable_colour(var):
    if var % r == 0:
        return r
    else:
        return var % r

#return position of variable (integer from [1, n])
#var = mapped variable
def variable_position(var):
    return math.ceil(var / 3)

#one position can be any of the given colours
def positive_clause(pos):
    clause = []
    for i in range(1, r + 1):
        clause.append(mapped_variable(i, pos))
    return clause

#three specified positions don't form a monochromatic solution
def negative_clause(col, x, y, z):
    clause = []
    clause.append(mapped_variable(col, x))
    clause.append(mapped_variable(col, y))
    clause.append(mapped_variable(col, z))
    clause = [-i for i in clause]
    return clause

#one position can't be a specified colour
def optional_clause(col, pos):
    clause = []
    for i in range(1, r + 1):
        if i != col:
            clause.append(mapped_variable(i, pos))
    clause = [-i for i in clause]
    return clause

#converts model to RGB string
def toWord(model):
    cols = ""
    for m in model:
        if m > 0:
            if m % 3 == 1:
                cols += "R"
            elif m % 3 == 2:
                cols += "G"
            elif m % 3 == 0:
                cols += "B"
    return cols

#consistency checking
def check(cols):
    for x in range(1, n + 1):
        for y in range(1, n + 1):
            if a*x + b*y <= c*n and (a*x + b*y) % c == 0:
                z = (a*x + b*y) // c
                if cols[x - 1] == cols[y - 1] and cols[y - 1] == cols[z - 1]:
                    return "Monochromatic Solution Found"
    return ""

with Solver(use_timer = True) as s:

    while True:

        #generate positive clauses
        for i in range(1, n + 1):
            s.add_clause(positive_clause(i)) #position can be any colour

        #generate negative clauses
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                if a*x + b*y <= c*n and (a*x + b*y) % c == 0:
                    z = (a*x + b*y) // c
                    s.add_clause(negative_clause(1, x, y, z)) #no positions are red
                    s.add_clause(negative_clause(2, x, y, z)) #no positions are green
                    s.add_clause(negative_clause(3, x, y, z)) #no positions are blue
        
        #generate optional clauses
        for i in range(1, n + 1):
            optional_clause(1, i) #position can't be green or blue
            optional_clause(2, i) #position can't be red or blue
            optional_clause(3, i) #position can't be red or green

        result = s.solve()
        end = time.time() #end timer

        #program exceeds five minutes
        if (end - start) >= 600.0:
            print("Timeout: %.2f seconds" % (end - start))
            break
        
        #no monochromatic solution found
        if result:
            cols = toWord(s.get_model())
            print("R > %d" % (n), cols, check(cols))

        #monochromatic solution found    
        else:
            print("R = %d" % (n))
            print("Time: %.2f seconds" % s.time_accum())
            break

        n += 1
