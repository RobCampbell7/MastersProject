from math import inf
from population import *
from solution import randTSP, objPos

# same as tests.py but only the 3 objective runs, logging every generation to <name>.txt for dfConversion
print("3d20c in progress")
cityNo = 20
dimensions = 3
graph = randTSP(cityNo, dimensions, 1, 1000)
iterationNo = 500
p = Population(cityNo, dimensions, graph, 100, 0.05, 0.5, iterationNo)
p.initialise()
objFile = open("3d20c.txt", "w")

prevPop = deepcopy(p)
prevHV = 0
for i in range(iterationNo):
    # one line per generation, solutions split by : and each one written as perm-objectives
    objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
    p.iterate()

# one more step after the loop so the last line logged is the final generation
p.iterate()

objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
objFile.close()
print("3d20c complete")

print("3d24c in progress")
cityNo = 24
dimensions = 3
graph = randTSP(cityNo, dimensions, 1, 1000)
iterationNo = 500
p = Population(cityNo, dimensions, graph, 100, 0.05, 0.5, iterationNo)
p.initialise()
objFile = open("3d24c.txt", "w")

prevPop = deepcopy(p)
prevHV = 0
for i in range(iterationNo):
    objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
    p.iterate()

p.iterate()

objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
objFile.close()
print("3d24c complete")

print("3d28c in progress")
cityNo = 28
dimensions = 3
graph = randTSP(cityNo, dimensions, 1, 1000)
iterationNo = 500
p = Population(cityNo, dimensions, graph, 250, 0.05, 0.5, iterationNo)
p.initialise()
objFile = open("3d28c.txt", "w")

prevPop = deepcopy(p)
prevHV = 0
for i in range(iterationNo):
    objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
    p.iterate()

p.iterate()

objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
objFile.close()
print("3d28c complete")

print("3d32c in progress")
cityNo = 32
dimensions = 3
graph = randTSP(cityNo, dimensions, 1, 1000)
iterationNo = 500
p = Population(cityNo, dimensions, graph, 250, 0.05, 0.5, iterationNo)
p.initialise()
objFile = open("3d32c.txt", "w")

prevPop = deepcopy(p)
prevHV = 0
for i in range(iterationNo):
    objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
    p.iterate()

p.iterate()

objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
objFile.close()
print("3d32c complete")