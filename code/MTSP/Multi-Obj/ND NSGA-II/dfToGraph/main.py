import pandas as pd
import plotly.express as px
import plotly.io as pio

def dominates(s1, s2):
    """
    Returns True iff s1 dominates s2
    """
    for i in range(len(s1)):
        if s1[i] > s2[i]:
            return False

    return s1 != s2

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


dimensions = [3, 4, 5]
cityNos = [20, 24, 28, 32]
for d in range(len(dimensions)):
    for c in range(len(cityNos)):
        fileName = str(dimensions[d]) + "d" + str(cityNos[c]) + "c"
        print(fileName + " in progress")
        df = pd.read_csv(fileName + ".csv")
        fig = px.scatter_3d(df, x="PC1", y="PC2", z="Iteration", color="maxF")
        fig.update_traces(marker_size=2.5, opacity=0.9)
        fig.update_layout(width=1200, height = 1200)
        fig.update_layout(scene_camera_eye=dict(x=0.0, y=2.0, z=0.1))
        pio.write_image(fig, fileName + 'p1.png', scale=5, width=800, height=600)
        fig.update_layout(scene_camera_eye=dict(x=2.0, y=0.1, z=0.1))
        pio.write_image(fig, fileName + 'p2.png', scale=5, width=800, height=600)
        fig.update_layout(scene_camera_eye=dict(x=0.0, y=0.0, z=2.0))
        pio.write_image(fig, fileName + 'p3.png', scale=5, width=800, height=600)
        fig.update_layout(scene_camera_eye=dict(x=2.0, y=-2.0, z=0.1))
        pio.write_image(fig, "" + fileName + 'p4.png', scale=5, width=800, height=600)
        print(fileName + " complete")