from math import inf
from population import *
from solution import randTSP, objPos

def repeatCount(lst):
    count = 0

    for i in lst:
        curFreq = lst.count(i)
        if(curFreq > count):
            count = curFreq
 
    return count

if __name__=="__main__":
    cityNo = 20
    graph = randTSP(cityNo, 1, 200)
    iterationNo = 400
    p = Population(cityNo, graph, 100, 0.15, 0.5, iterationNo)
    p.initialise()
    objFile = open("objFile.txt", "w")
    # objFile.write(":".join([str(s.perm) + "-" + str(s.objPos()) for s in p.pop]) + "\n")
    # objFile.write(":".join([str(s.objPos()) for s in p.pop]) + "\n")
    
    prevPop = deepcopy(p)
    prevHV = 0
    for i in range(iterationNo):
        newHV = p.hypervolume()
        print(p.hypervolume())
        # line = ":".join([str(s.objPos()) for s in p.pop])
        # one line per generation, each solution written as perm-objectives and split by ':'
        objFile.write(":".join([str(s.perm) + "-" + str(s.objPos()) for s in p.pop]) + "\n")
        # objFile.write(":".join([str(s.objPos()) for s in p.pop]) + "\n")
        # if newHV < prevHV:
        #     print("FUCK FUCK FUCK")
        #     break
        #     missing = []
        #     newFront = [s.perm for s in p.paretoFront()]
        #     for perm in prevFront:
        #         if perm not in newFront:
        #             missing.append(perm)
        #     assert missing == []
        prevHV = newHV
        # prevFront = [s.perm for s in p.paretoFront()]
        p.iterate()

    p.iterate()
    print(p.refPoint)
    
    objFile.write(":".join([str(s.perm) + "-" + str(s.objPos()) for s in p.pop]) + "\n")
    # objFile.write(":".join([str(s.objPos()) for s in p.pop]) + "\n")
    objFile.close()
    
    # front = p.paretoFront()
    # for s in front:
    #     print(repr(s.objPos()) + " - " + repr(s.perm))
