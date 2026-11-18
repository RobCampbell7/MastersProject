from copy import deepcopy
from math import atan2, inf
import random
from solution import Solution, objPos

def dominates(s1, s2):
    """
    Returns True iff s1 dominates s2
    """
    for i in range(len(s1)):
        if s1[i] > s2[i]:
            return False
        
    # no worse on any objective and not identical, so better on at least one (everything is minimised)
    return s1 != s2

# def incomparableTest(solutionSet):
#     for i in range(len(solutionSet)):
#         for j in range(len(solutionSet)):
#             if (weaklyDominates(solutionSet[i].objPos(), solutionSet[j].objPos()) or 
#                 weaklyDominates(solutionSet[j].objPos(), solutionSet[i].objPos())):
#                 return False
#     return True
    

def getFronts(remaining):
    if len(remaining) < 2:
        return [remaining]
    else:
        # non-dominated sorting, take off the current front then recurse on whatever is left
        front = []
        for i in range(len(remaining)):
            dominated = False
            j = 0
            while dominated == False and j < len(remaining):
                dominated = dominates(remaining[j].objPos(), remaining[i].objPos())
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

# sorting by angle puts a 2d front in order of rising f1 (and falling f2), which the hypervolume sum relies on
def sortFront(front):
    return sorted(front, key = lambda p : atan2(*p.objPos()))

def assignCrowdingDistances(front):
    front = sortFront(front)
    for s in front:
        s.crowdingDistance = 0
    
    # the ends of the front always survive
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
        nadir = [0, 0]
        # ref point for the hypervolume, half the total edge weight is well past the cost of any tour
        for _, (w1, w2) in self.d.items():
            nadir[0] += w1
            nadir[1] += w2
        self.refPoint = [nadir[0]//2 + epsilon, nadir[1]//2 + epsilon]

    def initialise(self):
        for i in range(self.popSize):
            self.pop.append(Solution(self.cityNo, self.d))
            self.pop[i].rand()

        self.findRefVec()
        self.inited = True

    def hypervolume(self):
        front = self.paretoFront()
        epsilon = 10 # TEMP - FIX THIS
        # add up the rectangles between each front point and the ref point, one slice of f2 at a time
        hv = (self.refPoint[0] - front[0].objPos(0)) * (self.refPoint[1] - front[0].objPos(1))
        for i in range(1, len(front)):
            hv += (self.refPoint[0] - front[i].objPos(0)) * (front[i - 1].objPos(1) - front[i].objPos(1))
            
        return hv

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

        return sortFront(front)

    def reproductiveSelection(self):
        matingPool = []
        mpSize = int(self.truncRate * self.popSize)
        # fill the mating pool a whole front at a time, the front that doesn't fit is cut down by crowding distance
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
        # elitist step, parents and offspring compete together for the next generation
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
            
            if set(self.pop[-1].perm) != set(range(1, self.cityNo)):
                print(self.pop[-1].perm)
                raise Exception("OH SHIT OH FUCK")
        
        # MERGE OFFSPRING AND OLDPOP, PICK BEST ( EVOLUTIONARY SELECTION )
        self.pop = deepcopy(self.evolutionarySelection(self.pop + offspring))
        self.iterNo += 1
