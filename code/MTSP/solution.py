from copy import deepcopy
from math import ceil
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
            d[arrange(i, j)] = random.randint(lower, higher)
    return d

# def crossover(p0, p1):
#     # subSize = random.randint(len(p0) / 4, len (p0) / 2)
#     subSize = 1 + ceil(len(p0)/2)
    
#     k = random.randint(0, len(p0) - subSize)
#     s0 = p0[k : k + subSize]
#     s1 = p1[k : k + subSize]
    
#     s = [s1[i] for i in range(subSize) if s1[i] not in s0]

#     p2 = []
#     for i in range(len(p1)):
#         if i >= k and i < k + subSize:
#             p2.append(p0[i])
#         elif p1[i] in s0:
#             # p2.append(s.pop(0))
#             p2.append(s.pop(random.randint(0, len(s) - 1)))
#         else:
#             p2.append(p1[i])
#     return p2

def crossover(p0, p1):
    s0 = p0[: len(p0) // 2]
    s1 = p1[: len(p0) // 2]
    
    s = [s1[i] for i in range(len(p0) // 2) if s1[i] not in s0]

    p2 = []
    for i in range(len(p1)):
        if i < len(p0) // 2:
            p2.append(p0[i])
        elif p1[i] in s0:
            p2.append(s.pop(0))
            # p2.append(s.pop(random.randint(0, len(s) - 1)))
        else:
            p2.append(p1[i])
    return p2

fitnessLookup = {}
def fitness(p, d):
    try:
        f = fitnessLookup[tuple(p)]
    except KeyError:
        f = d[0, p[0]] + d[0, p[-1]]
        for i in range(len(p)):
            f += d[arrange(p[i - 1], p[i])]
        fitnessLookup[tuple(p)] = f
    
    return f

# def mutate(p0):
#     i = random.randint(0, len(p0) - 1)
#     j = random.choice([j for j in range(len(p0)) if j != i])
#     p1 = deepcopy(p0)
#     p1[i], p1[j] = p1[j], p1[i]
#     return p1

def mutate(p0):
    i = random.randint(0, len(p0) - 2)
    j = random.choice([j for j in range(len(p0) - 1) if j < i - 1 or j > i + 1])
    p1 = deepcopy(p0)
    p1[i : i + 2], p1[j : j + 2] = p1[j : j + 2], p1[i : i + 2]
    return p1

class Solution:
    def __init__(self, cityNo, graph):
        self.cityNo = cityNo
        self.d = graph
        
    def rand(self):
        self.define(random.sample(range(1, self.cityNo), self.cityNo - 1))
    
    def define(self, perm):
        if len(perm) != self.cityNo - 1:
            raise Exception("len(perm) != self.cityNo - 1\n" + repr(self))
        else:
            self.perm = perm
            self.f = fitness(self.perm, self.d)
    
    def mutate(self):
        self.perm = mutate(self.perm)
        
    def crossover(self, ind):
        child = Solution(self.cityNo, self.d)
        child.define(crossover(self.perm, ind.perm))
        return child