"""
This program uses MDS on each individual generation separately
"""

import pandas as pd
from sklearn.manifold import MDS
import plotly.express as px
import numpy as np

def splitCoords(lst):
    splitLst = [[] for i in range(len(lst[0]))]
    for p in lst:
        for i in range(len(p)):
            splitLst[i].append(p[i])
    
    return splitLst

def weaklyDominates(s1, s2):
    """
    TODO -- FIX THIS PLEASE!!!
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

# def fastPareto(pop):
#     front = paretoFront(quickhull(pop))
#     for i in range(len(pop)):
#         if pop[i] not in front:
#             dominated = False
#             for j in range(len(front)):
#                 if dominates(front[j], pop[i]):
#                     dominated = True
#                     break

#             if dominated == False:
#                 front = [pop[i]] + [front[j] for j in range(len(front)) if not dominates(pop[i], front[j])]
    
#     return front

# def allocateParetoFlag(popData):
#     for i in range(len(popData["Iteration"])):
#         dominated = False
#         #         j += 1

#         for j in [k for k in range(len(popData["Iteration"])) if popData["Iteration"][k] == popData["Iteration"][i]]:
#             dominated = dominates((popData["f1"][j], popData["f2"][j]),
#                                   (popData["f1"][i], popData["f2"][i]))
#             if dominated == True:
#                 break
        
#         if dominated == False:
#             popData["inFront"][i] = True

# data = {
#     "f1" : [],
#     "f2" : [],
#     "Iteration" : [],
# }
points = []
with open("objFile.txt", "r") as objFile:
    i = -1
    for li in objFile.readlines():
        i += 1
        points.append([])
        for s in li.split(":"):
            permStr, coordStr = s.split("-")
            coord = eval(coordStr.replace(")", ", " + str(i) + ")"))
            points[-1].append(coord)
            # data["f1"].append(coord[0])
            # data["f2"].append(coord[1])
            # data["Iteration"].append(i)

# i = -1
# for gen in points:
#     i += 1
#     if i % 1 == 0:# and i < 10:
#         front = fastPareto(gen)
#         remaining = [p for p in gen if p not in front]
mds = MDS(n_components=2, random_state=0, normalized_stress="auto") 
transformedPoints = [mds.fit_transform(points[i]) for i in range(len(points))]

data = {
    "f1" : [],
    "f2" : [],
    "Iteration" : [],
}
i = -1
for row in transformedPoints:
    i += 1
    for p in row:
        data["f1"].append(p[0])
        data["f2"].append(p[1])
        data["Iteration"].append(i)

df = pd.DataFrame(data)

fig = px.scatter_3d(df, x="f1", y="f2", z="Iteration")
fig.update_traces(marker_size=3, opacity=1)
fig.update_layout(yaxis_range=[0,max(data["f2"])])
fig.update_layout(xaxis_range=[0,max(data["f1"])])
fig.show()