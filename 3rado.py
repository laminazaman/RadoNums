from pysat.solvers import Solver
import math
import time

r = 3 # number of colours
n = 3 # minimum value of n

# equation: ax + by = cz

# take constants a, b, and c as input
a = int(input())
b = int(input())
c = int(input())

start = time.time()

# return mapped variable (integer from [1, r * n])
# col = colour of variable, pos = position of variable
def mapped_variable(col, pos):
    return (pos - 1) * r + col

# return colour of variable (integer from [1, r])
# var = mapped variable
def variable_colour(var):
    if var % r == 0:
        return r
    else:
        return var % r

# return position of variable (integer from [1, n])
# var = mapped variable
def variable_position(var):
    return math.ceil(var / 3)

# one position can be any of the given colours
def positive_clause(pos):
    clause = []
    for i in range(1, r + 1):
        clause.append(mapped_variable(i, pos))
    return clause

# three specified positions don't form a monochromatic solution
def negative_clause(col, x, y, z):
    clause = []
    clause.append(mapped_variable(col, x))
    clause.append(mapped_variable(col, y))
    clause.append(mapped_variable(col, z))
    clause = [-i for i in clause]
    return clause

# one position can't be a specified colour
def optional_clause(col, pos):
    clause = []
    for i in range(1, r + 1):
        if i != col:
            clause.append(mapped_variable(i, pos))
    clause = [-i for i in clause]
    return clause

# return list of x, y, z values that satisfy ax + by = cz
def solve_equation(n):
    solutions = []
 
    x = n
    for y in range(1, n + 1):
        z = (a*x + b*y) // c
        if a*x + b*y == c*z and 1 <= z and z <= n:
            solutions.append((x, y, z))

    if a != b:
        y = n
        for x in range(1, n + 1):
            z = (a*x + b*y) // c
            if a*x + b*y == c*z and 1 <= z and z <= n:
                solutions.append((x, y, z))

    z = n
    for x in range(1, n + 1):
        y = (c*z - a*x) // b
        if a*x + b*y == c*z and 1 <= y and y <= n:
            solutions.append((x, y, z))

    return solutions

# consistency checking
def check(cols, n):
    equation_solutions = solve_equation(n)

    for i in range(len(equation_solutions)):
        x = equation_solutions[i][0]
        y = equation_solutions[i][1]
        z = equation_solutions[i][2]

        if cols[x - 1] == cols[y - 1] and cols[y - 1] == cols[z - 1]:
            return "Monochromatic Solution Found"
    
    return ""

# converts model to RGB string
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

# implement exact formulas for families of 3-colour Rado numbers
# Theorem 1.2 from ISAAC paper
def theorems():
    if a == 1 and b == -1 and c >= 1: # eqn: x - y = (m - 2)z
        m = c + 2
        return m**3 - m**2 - m - 1
    elif a == -b and c == a - 1 and a >= 3: # eqn: a(x - y) = (a - 1)z
        return a**3 + (a - 1)**2
    elif a == -b and c >= 1 and a >= c + 2 and math.gcd(a, c) == 1: # eqn: a(x - y) = bz
        return a**3
    else:
        return 0

# check that a theorem can be applied, output results
if theorems():
    end = time.time() #end timer
    print("R = %d" % (theorems()))
    print("Program Time: %.2f seconds" % (end - start))
    exit(1)

with Solver(use_timer = True) as s:

    # generate positive clauses for n = 1, 2
    s.add_clause(positive_clause(1))
    s.add_clause(positive_clause(2)) 

    # generate negative clauses for n = 1, 2
    sol1 = solve_equation(1)

    for i in range(len(sol1)):
        x = sol1[i][0]
        y = sol1[i][1]
        z = sol1[i][2]

        s.add_clause(negative_clause(1, x, y, z))
        s.add_clause(negative_clause(2, x, y, z)) 
        s.add_clause(negative_clause(3, x, y, z)) 

    sol2 = solve_equation(2)

    for i in range(len(sol2)):
        x = sol2[i][0]
        y = sol2[i][1]
        z = sol2[i][2]

        s.add_clause(negative_clause(1, x, y, z))
        s.add_clause(negative_clause(2, x, y, z)) 
        s.add_clause(negative_clause(3, x, y, z))

    # generate optional clauses for n = 1, 2
    s.add_clause(optional_clause(1, 1)) 
    s.add_clause(optional_clause(2, 1))
    s.add_clause(optional_clause(3, 1)) 

    s.add_clause(optional_clause(1, 2))
    s.add_clause(optional_clause(2, 2))
    s.add_clause(optional_clause(3, 2)) 

    while True:

        # generate positive clauses - position can be any colour
        s.add_clause(positive_clause(n))

        # list of x, y, z values that satisfy ax + by = cz
        equation_solutions = solve_equation(n)

        # generate negative clauses - avoid monochromatic solutions
        for i in range(len(equation_solutions)):
            x = equation_solutions[i][0]
            y = equation_solutions[i][1]
            z = equation_solutions[i][2]

            s.add_clause(negative_clause(1, x, y, z))
            s.add_clause(negative_clause(2, x, y, z)) 
            s.add_clause(negative_clause(3, x, y, z)) 

        # generate optional clauses - position can only be one colour
        s.add_clause(optional_clause(1, n)) 
        s.add_clause(optional_clause(2, n))
        s.add_clause(optional_clause(3, n)) 

        result = s.solve()
        end = time.time()

        # no monochromatic solution found
        if result:
            cols = toWord(s.get_model())
            print("R > %d" % (n), cols, check(cols, n))

        # monochromatic solution found    
        else:
            print("R = %d" % (n))
            print("SAT Time: %.2f seconds" % s.time_accum())
            print("Program Time: %.2f seconds" % (end - start))
            break

        n += 1
