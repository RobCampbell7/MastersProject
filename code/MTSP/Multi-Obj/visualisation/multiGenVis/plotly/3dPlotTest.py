from random import uniform
import pandas as pd
import plotly.express as px

import numpy as np

def splitCoords(lst):
    splitLst = [[] for i in range(len(lst[0]))]
    for p in lst:
        for i in range(len(p)):
            splitLst[i].append(p[i])
    
    return splitLst

def uniformPoints(flr = 1, ceil = 10):
    points = []
    for x in range(flr, ceil):
        for y in range(flr, ceil):
            for z in range(flr, ceil):
                points.append((x, y, z))

def randomPoints(n, flr = 1, ceil = 10):
    points = []
    for i in range(n):
        points.append(
            (uniform(flr, ceil), uniform(flr, ceil), uniform(flr, ceil))
        )
    return points

def gaussianPoints(n):
    points = np.random.normal(loc = 5, scale = 3, size = (n, 3))
    return [(x, y, z) for x, y, z in points]

points = gaussianPoints(2000)

data = {
    "perm" : [],
       "x" : [],
       "y" : [],
       "z" : [],
}
for p in points:
    data["perm"].append(None)
    data["x"].append(p[0])
    data["y"].append(p[1])
    data["z"].append(p[2])

df = pd.DataFrame(data)

fig = px.scatter_3d(df, x="x", y="y", z="z")
fig.update_traces(marker_size=2)
fig.show()
