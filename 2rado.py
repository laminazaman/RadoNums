from pysat.solvers import Solver

k = 2 # colours
n = 2 # start

# eqn: ax + by = cz

a = int(input())
b = int(input())
c = int(input())
    
def toWord(model):
    return "".join(["1" if x > 0 else "0" for x in model])
    
with Solver() as s:

    while True:

        for x in range(1, n + 1):
            for y in range(1, n + 1):
                z = (a*x + b*y) // c
                if a*x + b*y == c*z and 1 <= z and z <= n:
                    clause = [x, y, z]
                    s.add_clause(clause)
                    s.add_clause([-i for i in clause])

        result = s.solve()

        if result:
            print("R > %d" % (n), s.get_model())
        else:
            print("R = %d" % (n))
            break

        n += 1
