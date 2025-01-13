
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

def randTSP(cityNo, lower=0, higher=100):
    d = {}
    for i in range(cityNo):
        for j in range(i + 1, cityNo):
            d[arrange(i, j)] = (random.randint(lower, higher),
                                random.randint(lower, higher),
                                random.randint(lower, higher))
    return d

def obj(p, d):
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

x = np.array(randomPoints(10000, 10, 0, 200))
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