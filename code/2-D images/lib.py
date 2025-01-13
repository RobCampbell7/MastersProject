from copy import deepcopy
from math import atan2, ceil, inf
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.io as pio
import numpy as np
import random

def arrange(a, b):
    if a < b:
        return (a, b)
    else:
        return (b, a)

def randTSP(cityNo, dim, lower=0, higher=100):
    d = {}
    for i in range(cityNo):
        for j in range(i + 1, cityNo):
            d[arrange(i, j)] = tuple(random.randint(lower, higher)
                                     for i in range(dim))
    return d

def crossover(p0, p1):
    # subSize = random.randint(len(p0) / 4, len (p0) / 2)
    subSize = ceil(len(p0)/2)

    k = random.randint(0, len(p0) - subSize)
    s0 = p0[k : k + subSize]
    s1 = p1[k : k + subSize]

    s = [s1[i] for i in range(subSize) if s1[i] not in s0]

    # This messy list comprehension encapsulates the following functionality in the commented for
    # loop, this method allows for faster conversion to a tuple by keeping it all as one.
    # It is messy though so I've kept the original statement for readability
    p2 = tuple(
        p0[i] if i >= k and i < k + subSize
        else (s.pop(random.randint(0, len(s) - 1)) if p1[i] in s0 else p1[i])
        for i in range(len(p1))
    )
    # for i in range(len(p1)):
    #     if i >= k and i < k + subSize:
    #         p2.append(p0[i])
    #     elif p1[i] in s0:
    #         # p2.append(s.pop(0))
    #         p2.append(s.pop(random.randint(0, len(s) - 1)))
    #         sPointer += 1
    #     else:
    #         p2.append(p1[i])
    return p2

objectiveHash = {}
def objPos(p, d):
    try:
        return objectiveHash[p]
    except KeyError:
        dim = len(d[0, p[0]])
        f = [d[(0, p[0])][i] + d[(0, p[-1])][i] for i in range(dim)]

        for i in range(1, len(p)):
            c = arrange(p[i - 1], p[i])
            f = [f[i] + d[c][i] for i in range(dim)]
        objectiveHash[p] = f
    return f

def mutate(p0):
    i = random.randint(0, len(p0) - 1)
    j = random.choice([j for j in range(len(p0)) if j != i])
    p1 = tuple((p0[j] if k == i else p0[i]) if k in (i, j) else p0[k] for k in range(len(p0)))
    return p1

def flatten(lst2d):
    flatlst = []
    for row in lst2d:
        flatlst.extend(row)

    return flatlst

def removeRepeats(lst1D):
    found = []
    for p in lst1D:
        if p not in found:
            found.append(p)
    return found

def paretoFront(pop):
    front = []
    for i in range(len(pop)):
        dominated = False
        j = 0
        while dominated == False and j < len(pop):
            dominated = dominates(pop[j], pop[i])
            j += 1

        if dominated == False:
            front.append(pop[i])

    return front

class Solution:
    def __init__(self, cityNo, d):
        self.cityNo = cityNo
        self.d = d
        self.crowdingDistance = 0

    def rand(self):
        self.perm = tuple(random.sample(range(1, self.cityNo), self.cityNo - 1))
        if self.perm[0] > self.perm[-1]:
            self.perm = tuple(reversed(self.perm))

    def define(self, perm):
        if len(perm) != self.cityNo - 1:
            raise Exception("len(perm) != self.cityNo - 1\n" + repr(self))
        else:
            self.perm = perm

    def mutate(self):
        self.perm = mutate(self.perm)

    def crossover(self, ind):
        child = Solution(self.cityNo, self.d)
        child.define(crossover(self.perm, ind.perm))
        return child

    def objPos(self, m = -1):
        if m == -1:
            return objPos(self.perm, self.d)
        else:
            return objPos(self.perm, self.d)[m]

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
