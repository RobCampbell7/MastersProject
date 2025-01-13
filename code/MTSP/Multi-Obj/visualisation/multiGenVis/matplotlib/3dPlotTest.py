from random import uniform
import matplotlib.pyplot as plt
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

fig = plt.figure()
ax = fig.add_subplot(projection="3d")

points = gaussianPoints(2000)

ax.scatter(*splitCoords(points))

plt.show()
