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
    if len(points) == 0:
        return [], []
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

def quickHullR(p1: tuple[float, float], p2: tuple[float, float], points: list[tuple[float, float]], aboveFlag=True) -> list[tuple[float, float]]:
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
        hull.extend(quickHullR(p1, p3, p1Above, True))
        hull.extend(quickHullR(p3, p2, p2Above, True))
    else:
        hull.extend(quickHullR(p1, p3, p1Below, False))
        hull.extend(quickHullR(p3, p2, p2Below, False))
    
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
    aboveHull = quickHullR(p1, p2, above, True)
    belowHull = quickHullR(p1, p2, below, False)
    
    # Returns the convex hull, consisting of these two extreme points and the value of each
    # recursive instance
    return [p1, p2,*aboveHull, *belowHull]