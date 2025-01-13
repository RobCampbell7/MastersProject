import random
import timeit
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt

def lineDistance(p1:tuple[float, float], p2:tuple[float, float], p3:tuple[float, float]) -> float:
    """
    Finds the distance of a provided point, p3, from the line passing through p1 and p2.
    Using the formula |(x2-x1)(y1-yn) - (x1-xn)(y2-y1))| / (sqrt((x2-x1)^2 - (y2-y1)^2))
    """
    numer = abs((p2[0] - p1[0]) * (p1[1] - p3[1]) - (p1[0] - p3[0]) * (p2[1] - p1[1]))
    denom = sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[0])**2)
    return numer/denom

def createSegments(p1: tuple[float, float], p2: tuple[float, float], points: list[tuple[float, float]]):
    """
    Divides the list of points into two separate lists, based on whether or not they lie above or
    below the line that passes through p1 and p2.
    """
    # Defines the line that passes through p1 and p2 in the form y=mx+c
    m = (p2[1] - p1[1])/(p2[0] - p1[0])
    c = p1[1] - m * p1[0]

    above = []
    below = []
    for p in points:
        # If the point satisfies y > m*x + c, where y and x are the points that p consists of, then
        # the point is above the line. Otherwise the point is below the line. They are then added
        # to the corresponding list.
        if p[1] > m*p[0] + c:
            above.append(p)
        else:
            below.append(p)
    return above, below

def quickhullR(p1: tuple[float, float], p2: tuple[float, float], points: list[tuple[float, float]], aboveFlag=True) -> list[tuple[float, float]]:
    """
    The recursive part of the quickhull algorithm. It is passed two points, finds the point
    furthest from them and recures with this new point and the each of the old ones.
    
    The above flag idicates whether or not this instance is above or below the original line, this
    allows the program to know whether the above or below segment should be considered.
    """
    if points == []:
        # If there are no remaining points then there are no points to add to the convex hull
        return []

    # Sorts the points according to their distance from the line p1->p2
    sortedPoints = sorted(points, key = lambda p : lineDistance(p1, p2, p))
    p3 = sortedPoints.pop(-1) # Furthest point from line p1->p2, removed from the list of points
    hull = [p3] # Adds new point p3 to the hull
    
    p1Above, p1Below = createSegments(p1, p3, sortedPoints)
    p2Above, p2Below = createSegments(p3, p2, sortedPoints)
    
    # Recures with the new point and each of the old ones with the corresponding segment
    if aboveFlag == True:
        hull.extend(quickhullR(p1, p3, p1Above, True))
        hull.extend(quickhullR(p3, p2, p2Above, True))
    else:
        hull.extend(quickhullR(p1, p3, p1Below, False))
        hull.extend(quickhullR(p3, p2, p2Below, False))
    
    return hull

def quickhull(points: list[tuple[float, float]]) -> tuple[list[float], list[float]]:
    """
    This function is passed a list of points and returns their convex hull in the form of the
    points the hull consists of
    """
    # Sorts the points into order by their x-coordinate and selects the two extremes and removes
    # them from the list.
    sortedPoints = sorted(points, key=lambda p : p[0])
    p1 = sortedPoints.pop(0)
    p2 = sortedPoints.pop(-1)

    # Divides the list of points along this point running through the two extremes.
    above, below = createSegments(p1, p2, sortedPoints)
    # runs the recursive function on each side of this line, above and below
    aboveHull = quickhullR(p1, p2, above, True)
    belowHull = quickhullR(p1, p2, below, False)
    
    # Returns the convex hull, consisting of these two extreme points and the value of each
    # recursive instance
    return [p1, p2,*aboveHull, *belowHull]

def splitxy(points):
    x = []
    y = []
    for i in range(len(points)):
        x.append(points[i][0])
        y.append(points[i][1])
    return x, y

def randFloatCoords(n, D=2):
    return [tuple(random.uniform(0, 200) for i in range(D)) for i in range(n)]

def randIntCoords(n, D=2):
    return [tuple(random.randint(0, 200) for i in range(D)) for i in range(n)]

def createNormalPoints(n: int) -> list[tuple[float, float]]:
    """
    Creates a list of n points in 2 dimensions using a normal distribution around point.
    Uses mean of 500 and a standard deviation of 400.
    """
    points = np.random.normal(loc = 100, scale = 20, size = (n, 2))
    return [(x, y) for x, y in points]

def weaklyDominates(s1, s2):
    """
    returns True iff s1 weakly dominates s2
    """
    i = 0
    result = True
    while result == True and i < len(s1):
        if s2[i] <= s1[i]:
            result = False
        i += 1

    return result

def dominates(s1, s2):
    """
    returns True iff s1 dominates s2
    """
    return weaklyDominates(s1, s2) and (s1 != s2)

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

def fastPareto(pop):
    front = paretoFront(quickhull(pop))
    defIndex = len(front)
    for i in range(len(pop)):
        if pop[i] not in front:
            dominated = False
            for j in range(len(front)):
                if dominates(front[j], pop[i]):
                    dominated = True
                    break

            if dominated == False:
                front =  front[:defIndex] + [front[j] for j in range(defIndex, len(front)) if not dominates(pop[i], front[j])] + [pop[i]]
    
    return front

if __name__ == "__main__":
    allPoints = createNormalPoints(50000)
    # print("Original : " + str(timeit.timeit("paretoFront(createNormalPoints(2000))", number = 100, setup="from __main__ import paretoFront, createNormalPoints")))
    # print("    Fast : " + str(timeit.timeit("fastPareto(createNormalPoints(2000))", number = 100,  setup="from __main__ import fastPareto, createNormalPoints")))
    
    front1 = paretoFront(allPoints)
    front2 = fastPareto(allPoints)
    
    extras = [p for p in front2 if p not in front1]
    # if extras == []:
    #     print("AAAAAGGGGHHHHH")
    
    points = [p for p in allPoints if (p not in front1) and (p not in front2)]

    plt.plot(*splitxy(points), "k.")
    plt.plot(*splitxy(front1), "r.")
    plt.plot(*splitxy(extras), "b.")
    # plt.xlim(0, 100)
    # plt.ylim(0, 100)
    plt.show()
