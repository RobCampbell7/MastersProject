from math import inf
from population import *
from solution import randTSP, objPos

if __name__=="__main__":
    cityNo = 12
    dimensions = 3
    graph = randTSP(cityNo, dimensions, 1, 200)
    iterationNo = 100
    p = Population(cityNo, dimensions, graph, 50, 0.15, 0.5, iterationNo)
    p.initialise()
    objFile = open("objFile.txt", "w")
    
    prevPop = deepcopy(p)
    prevHV = 0
    for i in range(iterationNo):
        # one line per generation, each solution written as perm-objectives and split by ':'
        objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
        p.iterate()

    p.iterate()
    
    objFile.write(":".join([str(s.perm) + "-" + str(tuple(s.objPos())) for s in p.pop]) + "\n")
    objFile.close()