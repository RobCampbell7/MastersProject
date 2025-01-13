from copy import deepcopy
from math import ceil, inf
import random

def arrange(a, b):
    if a < b:
        return (a, b)
    else:
        return (b, a)

def randTSP(n, lower=0, higher=100):
    d = {}
    for i in range(n):
        for j in range(i + 1, n):
            d[arrange(i, j)] = (random.randint(lower, higher), random.randint(lower, higher))
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

# def crossover(p0, p1):
#     s0 = p0[: len(p0) // 2]
#     s1 = p1[: len(p0) // 2]
    
#     s = [s1[i] for i in range(len(p0) // 2) if s1[i] not in s0]

#     p2 = []
#     for i in range(len(p1)):
#         if i < len(p0) // 2:
#             p2.append(p0[i])
#         elif p1[i] in s0:
#             p2.append(s.pop(0))
#             # p2.append(s.pop(random.randint(0, len(s) - 1)))
#         else:
#             p2.append(p1[i])
#     return p2

objectiveHash = {}
def objPos(p, d):
    try:
        return objectiveHash[p]
    except KeyError:
        f1 = d[(0, p[0])][0] + d[(0, p[-1])][0]
        f2 = d[(0, p[0])][1] + d[(0, p[-1])][1]
        
        for i in range(1, len(p)):
            c = arrange(p[i - 1], p[i])
            f1 += d[c][0]
            f2 += d[c][1]

        objectiveHash[p] = (f1, f2)
        return (f1, f2)

# def mutate(p0):
#     i = random.randint(0, len(p0) - 1)
#     j = random.choice([j for j in range(len(p0)) if j != i])
#     p1 = deepcopy(p0)
#     p1[i], p1[j] = p1[j], p1[i]
#     return p1

def mutate(p0):
    i = random.randint(0, len(p0) - 1)
    j = random.choice([j for j in range(len(p0)) if j != i])
    p1 = tuple((p0[j] if k == i else p0[i]) if k in (i, j) else p0[k] for k in range(len(p0)))
    return p1

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