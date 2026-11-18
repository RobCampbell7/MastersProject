from itertools import permutations
import random
import plotly.express as px
import pandas as pd
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

def enumerateObj(cityNo, lower=0, higher = 100):
    graph = randTSP(cityNo, lower, higher)
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

data = {
    "f1" : [],
    "f2" : [],
    "f3" : [],
    "Iteration" : [],
}
# objective log from a 3 objective run, one line per generation
with open("objFile25.txt", "r") as objFile:
    i = -1
    for li in objFile.readlines():
        i += 1
        for s in li.split(":"):
            permStr, coordStr = s.split("-")
            coord = eval(coordStr.replace(")", ", " + str(i) + ")"))
            data["f1"].append(coord[0])
            data["f2"].append(coord[1])
            data["f3"].append(coord[2])
            data["Iteration"].append(i)

df = pd.DataFrame(data)
# one frame per generation, axes fixed to the largest values so the frames line up
fig = px.scatter_3d(df, x="f1", y="f2", z="f3", animation_frame="Iteration",
                    range_x=[0, max(data["f1"])], range_y=[0, max(data["f2"])], range_z=[0, max(data["f3"])])
fig.update_traces(marker_size=3, opacity=1)
fig.update_scenes(aspectmode='cube')
fig.show()
