from pysat.solvers import Solver

k = 3 #colours
n = 3 #start

#eqn: ax + by = cz

#take constants a, b, and c as input
a = int(input())
b = int(input())
c = int(input())

#function converts model to RGB string
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

with Solver() as s:

    while True:

        #positive clauses
        for i in range(1, n + 1):
            s.add_clause([3*i - 2, 3*i - 1, 3*i])

        #negative clauses
        for x in range(1, n + 1):
            for y in range(1, n + 1):
                if a*x + b*y <= c*n and (a*x + b*y) % c == 0:
                    z = (a*x + b*y) // c

                    red = [3*x - 2, 3*y - 2, 3*z - 2]
                    s.add_clause([-i for i in red])

                    green = [3*x - 1, 3*y - 1, 3*z - 1]
                    s.add_clause([-i for i in green])

                    blue = [3*x, 3*y, 3*z]
                    s.add_clause([-i for i in blue])
        
        #optional clauses
        for i in range(1, n + 1):
            s.add_clause([2 - 3*i, 1 - 3*i])
            s.add_clause([1 - 3*i, -3*i])
            s.add_clause([2 - 3*i, -3*i])

        result = s.solve()

        if result:
            print("R > %d" % (n), toWord(s.get_model()))
        else:
            print("R = %d" % (n)) #solution
            break

        n += 1
