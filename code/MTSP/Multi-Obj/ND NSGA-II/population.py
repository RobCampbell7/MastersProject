from copy import deepcopy
from math import atan2, inf
import random
from solution import Solution, objPos
from scipy.spatial import ConvexHull

def dominates(s1, s2):
    """
    Returns True iff s1 dominates s2
    """
    for i in range(len(s1)):
        if s1[i] > s2[i]:
            return False
        
    return s1 != s2

def getFronts(remaining):
    if len(remaining) < 2:
        return [remaining]
    else:
        front = []
        for i in range(len(remaining)):
            dominated = False
            j = 0
            while dominated == False and j < len(remaining):
                dominated = dominates(remaining[j].objPos(), remaining[i].objPos())
                j += 1
                
            if dominated == False:
                front.append(remaining[i])

        if len(remaining) == 0:
            return [front]
        else:
            return [front] + getFronts([remaining[i] for i in range(len(remaining)) if remaining[i] not in front])

def assignCrowdingDistances(front, dim):
    for s in front:
        s.crowdingDistance = 0

    for m in range(dim):
        front = sorted(front, key = lambda s : s.objPos(m))
        
        # fmax = max([s.objPos(m) for s in front])
        # fmin = min([s.objPos(m) for s in front])
        front[0].crowdingDistance = inf
        fmin = front[0].objPos(m)
        front[-1].crowdingDistance = inf
        fmax = front[-1].objPos(m)
        
        if fmax != fmin:
            for i in range(1, len(front) - 1):
                front[i].crowdingDistance += (front[i + 1].objPos(m) - front[i - 1].objPos(m))/(fmax - fmin)     

class Population:
    def __init__(self, cityNo, dim, graph, pop=20, mut=0.2, trunc=0.5, iterNo=1000):
        self.dim = dim
        self.cityNo = cityNo
        self.d = graph
        self.popSize = pop
        self.mutationRate = mut
        self.truncRate = trunc
        self.iterationMax = iterNo
        self.inited = False
        self.iterNo = 0
        self.pop = []

    def findRefVec(self, epsilon = 10):
        nadir = [0, 0]
        for _, (w1, w2) in self.d.items():
            nadir[0] += w1
            nadir[1] += w2
        return [nadir[0]//2 + epsilon, nadir[1]//2 + epsilon]

    def hvApprox(self):
        front = self.paretoFront()
        refVec = self.findRefVec
        N = 1000
        for _ in range(N):
            randCoord = [random.uniform(0, refVec[i]) for i in range(self.dim)]
            

    def initialise(self):
        for i in range(self.popSize):
            self.pop.append(Solution(self.cityNo, self.d))
            self.pop[i].rand()

        self.inited = True

    def paretoFront(self):
        pop = deepcopy(self.pop)
        front = []
        for i in range(len(pop)):
            dominated = False
            j = 0
            while dominated == False and j < len(pop):
                dominated = dominates(pop[j].objPos(), pop[i].objPos())
                j += 1

            if dominated == False:
                front.append(pop[i])

        return front

    def reproductiveSelection(self):
        matingPool = []
        mpSize = int(self.truncRate * self.popSize)
        fronts = getFronts(deepcopy(self.pop))

        for i in range(len(fronts)):
            remainingMPS = mpSize - len(matingPool)
            if remainingMPS == 0:
                break
            elif remainingMPS >= len(fronts[i]):
                matingPool.extend(fronts[i])
            else:
                assignCrowdingDistances(fronts[i], self.dim)
                fronts[i] = sorted(fronts[i], key = lambda s : s.crowdingDistance, reverse=True)
                matingPool.extend(fronts[i][:remainingMPS])
                break
        return matingPool
    
    def evolutionarySelection(self, combinedPop):
        selected = []
        fronts = getFronts(combinedPop)

        for i in range(len(fronts)):
            toSelect = self.popSize - len(selected)
            if toSelect == 0:
                break
            elif toSelect > len(fronts[i]):
                selected.extend(fronts[i])
            else:
                assignCrowdingDistances(fronts[i], self.dim)
                fronts[i] = sorted(fronts[i], key = lambda s : s.crowdingDistance, reverse=True)
                selected.extend(fronts[i][:toSelect])
                break
        return selected

    def iterate(self):
        if self.inited == False:
            raise RuntimeWarning("Population is not initialised")
        elif self.iterNo > self.iterationMax:
            raise RuntimeWarning("Iteration limit reached")
        
        offspring = []
        matingPool = self.reproductiveSelection()

        while len(offspring) < self.popSize:
            i = random.randint(0, len(matingPool) - 1)
            j = random.choice([j for j in range(len(matingPool)) if j != i])
            offspring.append(matingPool[i].crossover(matingPool[j]))

            if random.uniform(0, 1) > self.mutationRate:
                offspring[-1].mutate()
            
            if set(self.pop[-1].perm) != set(range(1, self.cityNo)):
                print(self.pop[-1].perm)
                raise Exception("OH SHIT OH FUCK")
        
        # MERGE OFFSPRING AND OLDPOP, PICK BEST ( EVOLUTIONARY SELECTION )
        self.pop = deepcopy(self.evolutionarySelection(self.pop + offspring))
        self.iterNo += 1
