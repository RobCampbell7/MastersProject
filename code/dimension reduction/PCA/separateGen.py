import pandas as pd
from sklearn.manifold import TSNE
import plotly.express as px
import numpy as np

def splitCoords(lst):
    splitLst = [[] for i in range(len(lst[0]))]
    for p in lst:
        for i in range(len(p)):
            splitLst[i].append(p[i])
    
    return splitLst

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
            # data["f1"].append(coord[0])
            # data["f2"].append(coord[1])
            # data["Iteration"].append(i)

# i = -1
# for gen in points:
#     i += 1
#     if i % 1 == 0:# and i < 10:
#         front = fastPareto(gen)
#         remaining = [p for p in gen if p not in front]
# tsne run on each generation by itself, so the layout isn't comparable between generations
tsne = TSNE(n_components=2, random_state=0, init="pca") 
transformedPoints = [tsne.fit_transform(np.asarray(points[i])) for i in range(len(points))]

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