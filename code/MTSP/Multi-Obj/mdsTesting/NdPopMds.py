
import random
from matplotlib import pyplot as plt
import numpy as np 
from sklearn.manifold import MDS 


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

def randTSP(cityNo, dim, lower=0, higher=100):
    d = {}
    for i in range(cityNo):
        for j in range(i + 1, cityNo):
            d[arrange(i, j)] = tuple(random.randint(lower, higher)
                                     for i in range(dim))
    return d

def obj(p, d):
    dim = len(d[0, p[0]])
    f = [d[(0, p[0])][i] + d[(0, p[-1])][i] for i in range(dim)]
    
    for i in range(1, len(p)):
        c = arrange(p[i - 1], p[i])
        f = [f[i] + d[c][i] for i in range(dim)]

    return f

def randomPoints(n, cityNo, dim, lower=0, higher=100):
    graph = randTSP(cityNo, dim, lower, higher)
    objPoints = []
    for i in range(n):
        objPoints.append(obj(random.sample(range(1, cityNo), cityNo - 1), graph))

    return objPoints

x = np.array(randomPoints(1000, 10, 4, 0, 200))
mds = MDS(n_components=2, random_state=0, normalized_stress="auto") 
  
# Fit the data to the MDS 
# object and transform the data 
X_transformed = mds.fit_transform(x)

xs = []
ys = []
for i in range(len(X_transformed)):
    xs.append(X_transformed[i][0])
    ys.append(X_transformed[i][1])

fig = plt.figure()
plt.plot(xs, ys, ".")
plt.show()