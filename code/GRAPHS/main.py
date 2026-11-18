import plotly.express as px
import plotly.io as pio
import pandas as pd
import numpy as np
from lib import *

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

print("optimisation began")
# objective vectors of every generation, starting with the random one
history = []
history.append([(tuple(s.objPos())) for s in p.pop])
for i in range(iterationNo):
    p.iterate()
    history.append([(tuple(s.objPos())) for s in p.pop])

p.iterate()
history.append([(tuple(s.objPos())) for s in p.pop])

print("optimisation complete")

# fit the pca once on every unique point from all generations so the axes are the same for each generation
pca = PCA(n_components=2)
pca = pca.fit(np.asarray(removeRepeats(flatten(history))))

data = {
    "PC1" : [],
    "PC2" : [],
    "Iteration" : [],
    "maxF" : [],
    "inFront" : []
}
for i in range(dimensions):
    data["f" + str(i + 1)] = []

for i in range(len(history)):
    front = paretoFront(history[i])
    transformedGen = pca.transform(history[i])

    for j in range(len(history[i])):
        for k in range(dimensions):
            data["f" + str(k + 1)].append(history[i][j][k])

        # which objective is largest for this solution (1 based), used to colour the plots
        data["maxF"].append(1 + max((range(len(history[i][j]))), key = lambda f : history[i][j][f]))
        data["Iteration"].append(i)
        data["PC1"].append(transformedGen[j][0])
        data["PC2"].append(transformedGen[j][1])
        data["inFront"].append(history[i][j] in front)
df = pd.DataFrame(data)
print("dataframe built")

fig = px.scatter_3d(df, x="PC1", y="PC2", z="Iteration", color="maxF")
fig.update_traces(marker_size=2.5, opacity=1)
fig.update_layout(width=1200, height = 1200)

print("creating images of plots")
filename = str(dimensions) + "d" + str(cityNo) + "c"
# same plot saved from four camera angles (1p to 4p), write_image needs kaleido
fig.update_layout(scene_camera_eye=dict(x=0.0, y=2.0, z=0.1))
pio.write_image(fig, filename + '1p.png', scale=5, width=800, height=600)
fig.update_layout(scene_camera_eye=dict(x=2.0, y=0.1, z=0.1))
pio.write_image(fig, filename + '2p.png', scale=5, width=800, height=600)
fig.update_layout(scene_camera_eye=dict(x=0.0, y=0.0, z=2.0))
pio.write_image(fig, filename + '3p.png', scale=5, width=800, height=600)
fig.update_layout(scene_camera_eye=dict(x=2.0, y=-2.0, z=0.1))
pio.write_image(fig, filename + '4p.png', scale=5, width=800, height=600)
print("images of plot created")
fig.show()