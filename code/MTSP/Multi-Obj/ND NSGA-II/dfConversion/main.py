import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

# minimisation, so s1 dominates if it is no worse anywhere and not identical
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
        history = []
        with open(fileName + ".txt", "r") as objFile:
            i = -1
            for li in objFile.readlines():
                i += 1
                history.append([])
                for s in li.split(":"):
                    permStr, coordStr = s.split("-")
                    # tack the generation number on the end of each objective tuple
                    coord = eval(coordStr.replace(")", ", " + str(i) + ")"))
                    history[-1].append(coord)
        data = {
            "PC1" : [],
            "PC2" : [],
            "Iteration" : [],
            "maxF" : [],
            "inFront" : []
        }
        for i in range(dimensions[d]):
            data["f" + str(i + 1)] = []

        # fit the pca once on every unique point from all generations so the axes are the same for each generation
        pca = PCA(n_components=2)
        pca = pca.fit(np.asarray(removeRepeats(flatten(history))))
        for i in range(len(history)):
            front = paretoFront(history[i])
            transformedGen = pca.transform(history[i])

            for j in range(len(history[i])):
                for k in range(dimensions[d]):
                    data["f" + str(k + 1)].append(history[i][j][k])

                # which objective is largest for this solution (1 based), used to colour the plots
                data["maxF"].append(1 + max((range(len(history[i][j]))), key = lambda f : history[i][j][f]))
                data["Iteration"].append(i)
                data["PC1"].append(transformedGen[j][0])
                data["PC2"].append(transformedGen[j][1])
                data["inFront"].append(history[i][j] in front)

        df = pd.DataFrame(data)
        df.to_csv(str(fileName) + ".csv")