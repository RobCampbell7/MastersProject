from math import inf
from population import *
from solution import randTSP

def repeatCount(lst):
    count = 0

    for i in lst:
        curFreq = lst.count(i)
        if(curFreq > count):
            count = curFreq
 
    return count

if __name__=="__main__":
    cityNo = 20
    graph = randTSP(cityNo, 1, 500)
    iterationNo = 100
    p = Population(cityNo, graph, 400, 0.4, 0.5, iterationNo)
    p.initialise()
    
    prevFront = [s.perm for s in p.paretoFront()]
    prevHV = 0
    for i in range(iterationNo):
        newHV = p.hypervolume()
        print(newHV)
        if newHV < prevHV:
            missing = []
            newFront = [s.perm for s in p.paretoFront()]
            for perm in prevFront:
                if perm not in newFront:
                    missing.append(perm)
            assert missing == []
        prevHV = newHV
        prevFront = [s.perm for s in p.paretoFront()]
        p.iterate()

    p.iterate()
    
    front = p.paretoFront()
    for s in front:
        print(repr(s.objPos()) + " - " + repr(s.perm))
