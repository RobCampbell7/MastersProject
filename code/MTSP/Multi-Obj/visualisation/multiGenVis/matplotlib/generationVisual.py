from quickhullAgain import quickhull
import matplotlib.pyplot as plt
import numpy as np

# turns a list of points into one list per axis, ready to * into scatter
def splitCoords(lst):
    splitLst = [[] for i in range(len(lst[0]))]
    for p in lst:
        for i in range(len(p)):
            splitLst[i].append(p[i])
    
    return splitLst

def weaklyDominates(s1, s2):
    """
    returns True iff s1 weakly dominates s2
    THIS IS SPECIFIC TO THE FILE "./multiGenVis/generationVisual.py"
    DO NOT COPY ELSEWHERE THIS IS A 2-OBJECTIVE IMPLEMENTATION
    """
    i = 0
    result = True
    while result == True and i < 2:
        if s2[i] <= s1[i]:
            result = False
        i += 1

    return result

def dominates(s1, s2):
    """
    returns True iff s1 dominates s2
    """
    return weaklyDominates(s1, s2) and (s1 != s2)

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

# points on the convex hull are a cheap first guess at the front, then every other point is checked against it
def fastPareto(pop):
    front = paretoFront(quickhull(pop))
    for i in range(len(pop)):
        if pop[i] not in front:
            dominated = False
            for j in range(len(front)):
                if dominates(front[j], pop[i]):
                    dominated = True
                    break

            if dominated == False:
                # pop[i] isn't dominated, so it joins the front and kicks out anything it dominates
                front = [pop[i]] + [front[j] for j in range(len(front)) if not dominates(pop[i], front[j])]
    
    return front

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

points = []
with open("objFile.txt", "r") as objFile:
    i = -1
    for li in objFile.readlines():
        i += 1
        # tack the generation number on as a third coordinate so each generation sits at its own height
        points.append([eval(coordStr.replace(")", ", " + str(i) + ")")) for coordStr in li.split(":")])

i = -1
for gen in points:
    i += 1
    if i % 1 == 0:# and i < 10:
        # front in red, the rest of the generation in blue
        front = fastPareto(gen)
        remaining = [p for p in gen if p not in front]
        ax.scatter(*splitCoords(front), c="r", marker = ".")
        # ax.scatter(11657, 10656, i, c="g")
        if len(remaining) > 0:
            ax.scatter(*splitCoords(remaining), c="b", marker = ".")

plt.show()
