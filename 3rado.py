from pysat.solvers import Solver

k = 3 #colours
n = 3 #start

#eqn: ax + by = cz

a = int(input())
b = int(input())
c = int(input())

"""
def colourList(n):
    vars = [i for i in range(1, n + 1)]
    vars += [i + n for i in range(1, n + 1)]
    vars += [i + 2*n for i in range(1, n + 1)]
    return vars

def setColour(cols, colour, pos):
    if colour == "red":
        cols[pos + n] *= -1
        cols[pos + 2*n] *= -1
    elif colour == "green":
        cols[pos - n] *= -1
        cols[pos + n] *= -1
    elif colour == "blue":
        cols[pos - 2*n] *= -1
        cols[pos - n] *= -1
    return cols
"""

with Solver() as s:

    while True:

        #cols = colourList(n)

        for x in range(1, n + 1):
            for y in range(1, n + 1):
                if a*x + b*y <= c*n and (a*x + b*y) % c == 0:
                    z = (a*x + b*y) // c

                    red = [x, y, z]
                    s.add_clause(red)
                    s.add_clause([-i for i in red])

                    green = [x + n, y + n, z + n]
                    s.add_clause(green)
                    s.add_clause([-i for i in green])

                    blue = [x + 2*n, y + 2*n, z + 2*n]
                    s.add_clause(blue)
                    s.add_clause([-i for i in blue])

        result = s.solve()

        if result:
            print("R > %d" % (n), s.get_model())
        else:
            print("R = %d" % (n))
            break

        n += 1