from itertools import permutations
import random
import matplotlib.pyplot as plt

def splitxy(points):
    x = []
    y = []
    for i in range(len(points)):
        x.append(points[i][0])
        y.append(points[i][1])
    return x, y

def arrange(a, b):
    if a < b:
        return (a, b)
    else:
        return (b, a)

def randTSP(cityNo, lower=0, higher=100):
    d = {}
    for i in range(cityNo):
        for j in range(i + 1, cityNo):
            d[arrange(i, j)] = (random.randint(lower, higher), random.randint(lower, higher))
    return d

def obj(p, d):
        # city 0 is the fixed start and isn't in the perm, so the tour is 0 -> p[0] -> ... -> p[-1] -> 0
        f1 = d[(0, p[0])][0] + d[(0, p[-1])][0]
        f2 = d[(0, p[0])][1] + d[(0, p[-1])][1]
        
        for i in range(1, len(p)):
            c = arrange(p[i - 1], p[i])
            f1 += d[c][0]
            f2 += d[c][1]

        return (f1, f2)

def randomPoints(n, cityNo, lower=0, higher = 100):
    graph = randTSP(cityNo, lower, higher)
    objPoints = []
    for i in range(n):
        objPoints.append(obj(random.sample(range(1, cityNo), cityNo - 1), graph))

    return objPoints

# def permNoRev(lst):
#     return [p for p in permutations(lst) if p[0] < p[-1]]
# def enumerateObj(cityNo, lower=0, higher = 100):
#     graph = randTSP(cityNo, lower, higher)
#     return [obj(p, graph) for p in permNoRev(range(1, cityNo))]


def enumerateObj(cityNo, lower=0, higher = 100):
    graph = randTSP(cityNo, lower, higher)
    # every tour starting at city 0, p[0] < p[-1] skips the reversed copy of each one
    return [obj(p, graph) for p in permutations(range(1, cityNo)) if p[0] < p[-1]]

def dominates(s1, s2):
    """
    Returns True iff s1 dominates s2
    """
    for i in range(len(s1)):
        if s1[i] > s2[i]:
            return False
        
    return s1 != s2

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

fullEnumeration = True
saveFigure = True
noOfPoints = 10000 # Ignore if fullEnumeration equals true
cityNo = 9

# full enumeration is (cityNo - 1)!/2 tours, fine for 9 cities but blows up fast
if fullEnumeration == True:
    allPoints = enumerateObj(cityNo, 1, 200)
    # with open(repr(cityNo) + "cities.txt", "w") as f:
    #     for p in allPoints:
    #         f.write(repr(p) + "\n")
else:
    allPoints = randomPoints(noOfPoints, cityNo)

front = paretoFront(allPoints)
points = [p for p in allPoints if p not in front]

plt.figure(figsize=(12, 12))
plt.plot(*splitxy(points), "k.")
plt.plot(*splitxy(front), "r.")
plt.grid()

if saveFigure == True:
    if fullEnumeration == True:
        fileName = "./tsp{0}cities.png".format(cityNo)
    else:
        fileName = "./tsp{0}cities{1}points.png".format(cityNo)
    plt.savefig(fileName, dpi=800, bbox_inches='tight')

# plt.close()
plt.show()
