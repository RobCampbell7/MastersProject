from copy import deepcopy
from math import atan2, inf
import random
from solution import Solution, objPos
from dominanceRelations import weaklyDominates, dominates
from quickhullForPareto import quickhull

def incomparableTest(solutionSet):
    for i in range(len(solutionSet)):
        for j in range(len(solutionSet)):
            if (weaklyDominates(solutionSet[i].objPos(), solutionSet[j].objPos()) or 
                weaklyDominates(solutionSet[j].objPos(), solutionSet[i].objPos())):
                return False
    return True

def getFronts(remaining):
    if len(remaining) < 2:
        return [remaining]
    else:
        front = []
        for i in range(len(remaining)):
            dominated = False
            j = 0
            while dominated == False and j < len(remaining):
                dominated = weaklyDominates(remaining[j].objPos(), remaining[i].objPos())
                j += 1
                
            if dominated == False:
                front.append(remaining[i])
            # for j in range(self.pop):
            #     if i != j:
            #         if weaklyDominates(self.pop[i].objPos(), self.pop[j].objPos()) == False:
            #             inFront = False
            #             break
            # if inFront == True:
            #     fronts[-1].append(self.pop[i])
        if len(remaining) == 0:
            return [front]
        else:
            return [front] + getFronts([remaining[i] for i in range(len(remaining)) if remaining[i] not in front])

def paretoFront(pop):
    front = []
    for i in range(len(pop)):
        dominated = False
        j = 0
        while dominated == False and j < len(pop):
            dominated = dominates(pop[i].objPos(), pop[i].objPos())
            j += 1

        if dominated == False:
            front.append(pop[i])

    return front

# def fastPareto(pop):
#     return paretoFront(quickhull(deepcopy(pop)))

# def getFronts(pop):
#     fronts = []
#     points = deepcopy(pop)
#     while len(points > 0):
#         fronts.append(fastPareto(points))
#         points = [p for p in points if p not in fronts[-1]]
    
#     return fronts

def sortFront(front):
    return sorted(front, key = lambda p : atan2(*p.objPos()))

def assignCrowdingDistances(front):
    front = sortFront(front)
    for s in front:
        s.crowdingDistance = 0
    
    front[0].crowdingDistance = front[-1].crowdingDistance = inf

    for m in range(2):
        fmax = max([s.objPos(m) for s in front])
        fmin = min([s.objPos(m) for s in front])
        if fmax != fmin:
            for i in range(1, len(front) - 1):
                front[i].crowdingDistance += (front[i + 1].objPos(m) - front[i - 1].objPos(m))/(fmax - fmin)     

class Population:
    def __init__(self, cityNo, graph, pop=20, mut=0.2, trunc=0.5, iterNo=1000):
        self.cityNo = cityNo
        self.d = graph
        self.popSize = pop
        self.mutationRate = mut
        self.truncRate = trunc
        self.iterationMax = iterNo
        self.inited = False
        self.iterNo = 0
        self.pop = []

    # def findRefVec(self, epsilon = 10):
    #     nadir = [0, 0]
    #     for i in range(1000):
    #         new = tuple(random.sample(range(self.cityNo), self.cityNo))
    #         nadir[0] = max(objPos(new, self.d)[0], nadir[0])
    #         nadir[1] = max(objPos(new, self.d)[1], nadir[1])
        
    #     self.refPoint = [nadir[0] + epsilon, nadir[1] + epsilon]

    def findRefVec(self, epsilon = 10):
        nadir = [epsilon, epsilon]
        for _, (w1, w2) in self.d.items():
            nadir[0] += w1
            nadir[1] += w2
        self.refPoint = nadir

    def initialise(self):
        for i in range(self.popSize):
            self.pop.append(Solution(self.cityNo, self.d))
            self.pop[i].rand()

        self.findRefVec()
        self.inited = True

    def hypervolume(self):
        front = self.paretoFront()
        epsilon = 10 # TEMP - FIX THIS
        hv = (self.refPoint[0] - front[0].objPos(0)) * (self.refPoint[1] - front[0].objPos(1))
        for i in range(len(front)):
            hv += (self.refPoint[0] - front[i].objPos(0)) * (front[i - 1].objPos(1) - front[i].objPos(1))
            
        return hv

    def paretoFront(self):
        pop = deepcopy(self.pop)
        front = []
        for i in range(len(pop)):
            dominated = False
            j = 0
            while dominated == False and j < len(pop):
                dominated = weaklyDominates(pop[j].objPos(), pop[i].objPos())
                j += 1

            if dominated == False:
                front.append(pop[i])

        return sortFront(front)

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
                assignCrowdingDistances(fronts[i])
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
                assignCrowdingDistances(fronts[i])
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
            
            if set(self.pop[-1].perm) != set(range(self.cityNo)):
                print(self.pop[-1].perm)
                raise Exception("OH SHIT OH FUCK")
        
        # MERGE OFFSPRING AND OLDPOP, PICK BEST ( EVOLUTIONARY SELECTION )
        self.pop = deepcopy(self.evolutionarySelection(self.pop + offspring))
        self.iterNo += 1
