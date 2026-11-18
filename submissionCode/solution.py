from math import ceil, inf
import random

# edges are stored once with the smaller city first, so (a, b) and (b, a) hit the same key
def arrange(a, b):
    if a < b:
        return (a, b)
    else:
        return (b, a)

# fully connected graph, every edge gets a random weight for each of the dim objectives
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

    # child keeps a block of p0 in the same place, the rest comes from p1 in order
    k = random.randint(0, len(p0) - subSize)
    s0 = p0[k : k + subSize]
    s1 = p1[k : k + subSize]

    # cities in p1's block that p0's block doesn't have, used to fill the spots where p1 clashes with the block
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

# cache of objective vectors by perm, perms are tuples so they work as keys
objectiveHash = {}
def objPos(p, d):
    try:
        return objectiveHash[p]
    except KeyError:
        dim = len(d[0, p[0]])
        # city 0 is the fixed start and isn't in the perm, so the tour is 0 -> p[0] -> ... -> p[-1] -> 0
        f = [d[(0, p[0])][i] + d[(0, p[-1])][i] for i in range(dim)]

        for i in range(1, len(p)):
            c = arrange(p[i - 1], p[i])
            f = [f[i] + d[c][i] for i in range(dim)]
        objectiveHash[p] = f
    return f

def mutate(p0):
    i = random.randint(0, len(p0) - 1)
    j = random.choice([j for j in range(len(p0)) if j != i])
    # swap two random cities
    p1 = tuple((p0[j] if k == i else p0[i]) if k in (i, j) else p0[k] for k in range(len(p0)))
    return p1

class Solution:
    def __init__(self, cityNo, d):
        self.cityNo = cityNo
        self.d = d
        self.crowdingDistance = 0

    def rand(self):
        self.perm = tuple(random.sample(range(1, self.cityNo), self.cityNo - 1))
        # a tour and its reverse cost the same, so only keep one direction
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