from randomVisual import paretoFront, createNormalPoints, quickhull, dominates
import timeit

def oldFastPareto(pop):
    front = paretoFront(quickhull(pop))
    for i in range(len(pop)):
        if pop[i] not in front:
            dominated = False
            for j in range(len(front)):
                if dominates(front[j], pop[i]):
                    dominated = True
                    break

            if dominated == False:
                front = [pop[i]] + [front[j] for j in range(len(front)) if not dominates(pop[i], front[j])]
    
    return front

def newFastPareto(pop):
    front = paretoFront(quickhull(pop))
    pseudoFront = []
    defIndex = len(front)
    for i in range(len(pop)):
        if pop[i] not in front:
            dominated = False
            for j in range(len(front)):
                if dominates(front[j], pop[i]):
                    dominated = True
                    break

            if dominated == False:
                pseudoFront.append(pop[i])

    return front + paretoFront(pseudoFront)
    
print("old time : " + str(timeit.timeit("oldFastPareto(createNormalPoints(100000))", number = 10, setup="from __main__ import oldFastPareto, createNormalPoints")))
print("new time : " + str(timeit.timeit("newFastPareto(createNormalPoints(100000))", number = 10, setup="from __main__ import newFastPareto, createNormalPoints")))