"""
This program uses tsne on each individual generation separately
"""
import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import plotly.express as px
import numpy as np

def splitCoords(lst):
    splitLst = [[] for i in range(len(lst[0]))]
    for p in lst:
        for i in range(len(p)):
            splitLst[i].append(p[i])
    
    return splitLst

def weaklyDominates(s1, s2):
    i = 0
    result = True
    while result == True:
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

def flatten(lst2d):
    flatlst = []
    for row in lst2d:
        flatlst.extend(row)
    
    return flatlst

points = []
with open("objFile.txt", "r") as objFile:
    i = -1
    for li in objFile.readlines():
        i += 1
        points.append([])
        for s in li.split(":"):
            permStr, coordStr = s.split("-")
            # tack the generation number on the end of each objective tuple
            coord = eval(coordStr.replace(")", ", " + str(i) + ")"))
            points[-1].append(coord)

# fit on every generation at once then transform each one, so all generations share the same two axes
pca = PCA(n_components=2) # OTHER ARGUMENTS TOO PROBABLY
pca.fit(np.asarray(flatten(points)))
transformedPoints = [pca.transform(np.asarray(points[i])) for i in range(len(points))]

# transformedPoints = []
# for j in len(points):
#     transformedPoints.append([])
#     transformedPoints[-1].append(points[j * len(points[0]) : (j + 1) * len(points[0])])

data = {
    "PC1" : [],
    "PC2" : [],
    "Iteration" : [],
}
i = -1
for row in transformedPoints:
    i += 1
    for p in row:
        data["PC1"].append(p[0])
        data["PC2"].append(p[1])
        data["Iteration"].append(i)

df = pd.DataFrame(data)
df.save_csv()

# fig = px.scatter_3d(df, x="PC1", y="PC2", z="Iteration")
# fig.update_traces(marker_size=3, opacity=1)
# fig.update_layout(yaxis_range=[0,max(data["PC2"])])
# fig.update_layout(xaxis_range=[0,max(data["PC1"])])
# fig.show()