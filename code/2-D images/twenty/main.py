from copy import deepcopy
from math import atan2, ceil, inf
import pandas as pd
from sklearn.decomposition import PCA
import plotly.express as px
import plotly.io as pio
import numpy as np
import random
from lib import *

cityNo = 20
dimensions = 2
lowerWeightBound = 1
upperWeightBound = 1000
iterationNo = 250
populationSize = 100
mutationRate = 0.05
truncationRate = 0.5

graph = randTSP(cityNo, dimensions, lowerWeightBound, upperWeightBound)
p = Population(cityNo, dimensions, graph, populationSize, mutationRate, truncationRate, iterationNo)
p.initialise()

history = []
history.append([(tuple(s.objPos())) for s in p.pop])
for i in range(iterationNo):
    print("iteration: " + str(i + 1))
    p.iterate()
    history.append([(tuple(s.objPos())) for s in p.pop])

p.iterate()
history.append([(tuple(s.objPos())) for s in p.pop])

pca = PCA(n_components=2)
pca = pca.fit(np.asarray(removeRepeats(flatten(history))))

data = {
    "F1" : [],
    "F2" : [],
    "Iteration" : [],
    "maxF" : [],
}
paretoData = {
    "F1" : [],
    "F2" : [],
    "Iteration" : [],
    "maxF" : []
}

for i in range(len(history)):
    for j in range(len(history[i])):
        data["maxF"].append(1 + max((range(len(history[i][j]))), key = lambda f : history[i][j][f]))
        data["Iteration"].append(i)
        data["F1"].append(history[i][j][0])
        data["F2"].append(history[i][j][1])
df = pd.DataFrame(data)
df.to_csv("simple.csv")

for i in range(len(history)):
    front = paretoFront(history[i])
    for j in range(len(history[i])):
        if history[i][j] in front:
            paretoData["maxF"].append(1 + max((range(len(history[i][j]))), key = lambda f : history[i][j][f]))
            paretoData["Iteration"].append(i)
            paretoData["F1"].append(history[i][j][0])
            paretoData["F2"].append(history[i][j][1])
paretodf = pd.DataFrame(paretoData)
paretodf.to_csv("pareto.csv")

fig1 = px.scatter_3d(df, x="F1", y="F2", z="Iteration")
fig1.update_traces(marker_size=2.5, opacity=0.9)
fig1.update_layout(width=1200, height = 1200)
print("Figure 1 created")
fig1.update_layout(scene_camera_eye=dict(x=0.0, y=2.0, z=0.1))
pio.write_image(fig1, 'simpleImage1.png', scale=5, width=800, height=600)
print("First image saved")
fig1.update_layout(scene_camera_eye=dict(x=2.0, y=0.1, z=0.1))
pio.write_image(fig1, 'simpleImage2.png', scale=5, width=800, height=600)
print("Second image saved")
fig1.update_layout(scene_camera_eye=dict(x=0.0, y=0.0, z=2.0))
pio.write_image(fig1, 'simpleImage3.png', scale=5, width=800, height=600)
print("Third image saved")
fig1.update_layout(scene_camera_eye=dict(x=2.0, y=-2.0, z=0.1))
pio.write_image(fig1, 'simpleImage4.png', scale=5, width=800, height=600)
print("Fourth image saved")

fig2 = px.scatter_3d(paretodf, x="F1", y="F2", z="Iteration")
fig2.update_traces(marker_size=2.5, opacity=0.9)
fig2.update_layout(width=1200, height = 1200)
print("\nFigure 2 created")

fig2.update_layout(scene_camera_eye=dict(x=0.0, y=2.0, z=0.1))
pio.write_image(fig2, 'paretoImage1.png',scale=5, width=800, height=600)
print("First image saved")

fig2.update_layout(scene_camera_eye=dict(x=2.0, y=0.1, z=0.1))
pio.write_image(fig2, 'paretoImage2.png',scale=5, width=800, height=600)
print("Second image saved")

fig2.update_layout(scene_camera_eye=dict(x=0.0, y=0.0, z=2.0))
pio.write_image(fig2, 'paretoImage3.png',scale=5, width=800, height=600)
print("Third image saved")

fig2.update_layout(scene_camera_eye=dict(x=2.0, y=-2.0, z=0.1))
pio.write_image(fig2, 'paretoImage4.png',scale=5, width=800, height=600)
print("Fourth image saved")