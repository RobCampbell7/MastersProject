import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from population import Population
from solution import randTSP

def flatten(lst2d):
    flatlst = []
    for row in lst2d:
        flatlst.extend(row)

    return flatlst

def removeRepeats(lst1D):
    found = []
    for p in lst1D:
        if p not in found:
            found.append(p)
    return found

cityNo = 30
dimensions = 3
lowerWeightBound = 1
upperWeightBound = 1000
iterationNo = 500
populationSize = 100
mutationRate = 0.05
truncationRate = 0.5

graph = randTSP(cityNo, dimensions, lowerWeightBound, upperWeightBound)
p = Population(cityNo, dimensions, graph, populationSize, mutationRate, truncationRate, iterationNo)
p.initialise()

history = []
history.append([(tuple(s.objPos())) for s in p.pop])
for i in range(iterationNo):
    p.iterate()
    history.append([(tuple(s.objPos())) for s in p.pop])

p.iterate()
history.append([(tuple(s.objPos())) for s in p.pop])

# fit the pca on every distinct objective vector from the whole run so all generations share the same axes
pca = PCA(n_components=2)
pca = pca.fit(np.asarray(removeRepeats(flatten(history))))

data = {
    "PC1" : [],
    "PC2" : [],
    "Iteration" : [],
    "maxF" : []
}

for i in range(len(history)):
    transformedGen = pca.transform(history[i])
    for j in range(len(history[i])):
        # maxF is which objective (counting from 1) is largest for that solution, used for the colour
        data["maxF"].append(1 + max((range(len(history[i][j]))), key = lambda f : history[i][j][f]))
        data["Iteration"].append(i)
        data["PC1"].append(transformedGen[j][0])
        data["PC2"].append(transformedGen[j][1])

df = pd.DataFrame(data)

# generation number on the z axis so you can see the population move over the run
fig = px.scatter_3d(df, x="PC1", y="PC2", z="Iteration", color="maxF")
fig.update_traces(marker_size=2.5, opacity=1)
fig.show()