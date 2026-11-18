from math import inf

# recursive insert so nodes stays sorted
def insert(lst, item):
    if len(lst) == 0 or lst[-1] <= item:
        return lst + [item]
    else:
        return insert(lst[:-1], item) + lst[-1:]

class Graph:
    def __init__(self):
        self.paths = {} # Type dict((int, int) : float)
        self.nodes = [] # Type list(int)
        
    def addNode(self, node):
        self.nodes = insert(self.nodes, node)

    def addPath(self, node1, node2, distance):
        if node1 not in self.nodes:
            self.addNode(node1)
        if node2 not in self.nodes:
            self.addNode(node2)
        
        self.paths[(node1, node2)] = distance
    
    def getDist(self, node1, node2):
        try:
            return self.paths({node1, node2})
        except KeyError:
            if node1 not in self.nodes:
                raise Exception(repr(node1) + " is not a valid graph node")
            if node2 not in self.nodes:
                raise Exception(repr(node1) + " is not a valid graph node")
            else:
                return inf