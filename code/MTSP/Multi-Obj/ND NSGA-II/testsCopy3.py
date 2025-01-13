from math import inf
from population import *
from solution import randTSP, objPos

print("5d20c in progress")
cityNo = 20
dimensions = 5
graph = randTSP(cityNo, dimensions, 1, 1000)
iterationNo = 500
p = Population(cityNo, dimensions, graph, 100, 0.05, 0.5, iterationNo)
p.initialise()
objFile = open("5d20c.txt", "w")

prevPop = deepcopy(p)
prevHV = 0
for i in range(iterationNo):
    objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
    p.iterate()

p.iterate()

objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
objFile.close()
print("5d20c complete")

print("5d24c in progress")
cityNo = 24
dimensions = 5
graph = randTSP(cityNo, dimensions, 1, 1000)
iterationNo = 500
p = Population(cityNo, dimensions, graph, 80, 0.05, 0.5, iterationNo)
p.initialise()
objFile = open("5d24c.txt", "w")

prevPop = deepcopy(p)
prevHV = 0
for i in range(iterationNo):
    objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
    p.iterate()

p.iterate()

objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
objFile.close()
print("5d24c complete")

print("5d28c in progress")
cityNo = 28
dimensions = 5
graph = randTSP(cityNo, dimensions, 1, 1000)
iterationNo = 500
p = Population(cityNo, dimensions, graph, 80, 0.05, 0.5, iterationNo)
p.initialise()
objFile = open("5d28c.txt", "w")

prevPop = deepcopy(p)
prevHV = 0
for i in range(iterationNo):
    objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
    p.iterate()

p.iterate()

objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
objFile.close()
print("5d28c complete")

print("5d32c in progress")
cityNo = 32
dimensions = 5
graph = randTSP(cityNo, dimensions, 1, 1000)
iterationNo = 500
p = Population(cityNo, dimensions, graph, 100, 0.05, 0.5, iterationNo)
p.initialise()
objFile = open("5d32c.txt", "w")

prevPop = deepcopy(p)
prevHV = 0
for i in range(iterationNo):
    objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
    p.iterate()

p.iterate()

objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
objFile.close()
print("5d32c complete")