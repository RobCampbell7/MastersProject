"""
There's no real reason for me to do this, just basically interested
"""
from itertools import permutations
import random
import matplotlib.pyplot as plt
import numpy as np

def splitCoords(lst):
    splitLst = [[] for i in range(len(lst[0]))]
    for p in lst:
        for i in range(len(p)):
            splitLst[i].append(p[i])
    
    return splitLst

def arrange(a, b):
    if a < b:
        return (a, b)
    else:
        return (b, a)

# same as the solution.py version but with three weights per edge
def randTSP(cityNo, lower=0, higher=100):
    d = {}
    for i in range(cityNo):
        for j in range(i + 1, cityNo):
            d[arrange(i, j)] = (random.randint(lower, higher),
                                random.randint(lower, higher),
                                random.randint(lower, higher))
    return d

def obj(p, d):
    # city 0 is the fixed start and isn't in the perm, so the tour is 0 -> p[0] -> ... -> p[-1] -> 0
    f1 = d[(0, p[0])][0] + d[(0, p[-1])][0]
    f2 = d[(0, p[0])][1] + d[(0, p[-1])][1]
    f3 = d[(0, p[0])][2] + d[(0, p[-1])][2]
    
    for i in range(1, len(p)):
        c = arrange(p[i - 1], p[i])
        f1 += d[c][0]
        f2 += d[c][1]
        f3 += d[c][2]

    return (f1, f2, f3)

def randomPoints(n, cityNo, lower=0, higher = 100):
    graph = randTSP(cityNo, lower, higher)
    objPoints = []
    for i in range(n):
        objPoints.append(obj(random.sample(range(1, cityNo), cityNo - 1), graph))

    return objPoints

# def permNoRev(lst):
#     noRepPerms = []
#     for p in permutations(lst):
#         if p not in noRepPerms and p[::-1] not in noRepPerms:
#             noRepPerms.append(p)
#     return noRepPerms

# def permNoRev(lst):
#     return [p for p in permutations(lst) if p[0] < p[-1]]

def enumerateObj(cityNo, lower=0, higher = 100):
    graph = randTSP(cityNo, lower, higher)
    # every tour starting at city 0, p[0] < p[-1] skips the reversed copy of each one
    return [obj(p, graph) for p in permutations(range(1, cityNo)) if p[0] < p[-1]]

def dominates(s1, s2):
    """
    Returns True iff s1 dominates s2
    """
    for i in range(len(s1)):
        if s1[i] > s2[i]:
            return False
        
    return s1 != s2

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

fullEnumeration = True
saveFigure = True
noOfPoints = 10000 # Ignore if fullEnumeration equals true
cityNo = 9

if fullEnumeration == True:
    points = enumerateObj(cityNo, 1, 200)
    # with open(repr(cityNo) + "cities.txt", "w") as f:
    #     for p in points:
    #         f.write(repr(p) + "\n")
else:
    points = randomPoints(noOfPoints, cityNo)

front1 = paretoFront(points)
points = [p for p in points if p not in front1]
# front2 = paretoFront(points)
# points = [p for p in points if p not in front2]
# front3 = paretoFront(points)
# points = [p for p in points if p not in front3]
# front4 = paretoFront(points)
# points = [p for p in points if p not in front4]
# front5 = paretoFront(points)
# points = [p for p in points if p not in front5]

# for s1 in front1:
#     for s2 in front2:
#         if dominates(s2, s1) == True:
#             print("OH FUCKING SHIT")

fig = plt.figure(figsize=(12, 12))
ax = fig.add_subplot(projection="3d")

plt.margins(tight=True)
ax.scatter(*splitCoords(front1), "b.")
ax.scatter(*splitCoords(points), "r.")


plt.show()
