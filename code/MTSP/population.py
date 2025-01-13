from copy import deepcopy
import random
from solution import Solution

class Population:
    def __init__(self, cityNo, graph, pop=20, mut=0.2, trunc=0.5, iterNo=1000, keepBest = 3):
        self.cityNo = cityNo
        self.d = graph
        self.popSize = pop
        self.mutationRate = mut
        self.truncRate = trunc
        self.iterationMax = iterNo
        self.inited = False
        self.iterNo = 0
        self.pop = []
        self.keepBest = keepBest

    def repeatNo(self):
        self.pop = sorted(self.pop, key = lambda s : s.f)
        current = deepcopy(self.pop[0])
        currentRepNo = 1
        maximum = deepcopy(self.pop[0])
        maxRepNo = 1

        for i in range(1, self.popSize):
            if current == self.pop[i]:
                currentRepNo += 1
                if currentRepNo > maxRepNo:
                    maxRepNo = currentRepNo
                    maximum = deepcopy(current)
            else:
                currentRepNo = 1
                current = deepcopy(self.pop[i])
        return maxRepNo

    def best(self):
        bestInd = min(self.pop, key = lambda x: x.f)
        return bestInd.perm, bestInd.f

    def initialise(self):
        for i in range(self.popSize):
            self.pop.append(Solution(self.cityNo, self.d))
            self.pop[i].rand()
        self.inited = True
    
    # def selection(self):
    #     """
    #     (poorly) Implementes roulette wheel selection of 2 individuals from population 
    #     """
    #     self.pop.sort(key = lambda s : s.f)
    #     selected = []
        
    #     while len(selected) < self.truncRate * self.popSize:
    #         selected.append(self.selectOne())
        
    #     return selected
    
    # def selectOne(self):
    #     selected = None
    #     fMax = max([s.f for s in self.pop])
    #     fSum = sum([(fMax - s.f) for s in self.pop])
        
    #     p = random.uniform(0, fSum - 1)
    #     current = 0
    #     for s in self.pop:
    #         current += (fMax - s.f)
    #         if current > p:
    #             selected = s
    #             break
        
    #     return selected

    def selection(self):
        """
        Implementes tournament selection of 2 individuals from population
        """
        selected = []
        while len(selected) < self.truncRate * self.popSize:
            i = random.randint(0, self.popSize - 1)
            j = random.choice([j for j in range(self.popSize) if j != i])

            if self.pop[i].f < self.pop[j].f:
                selected.append(self.pop[i])
            else:
                selected.append(self.pop[j])

        return selected
    
    # def selection(self):
    #     """
    #     Simple random selection
    #     """
    #     selectionNo = int(self.popSize * self.truncRate)
    #     self.pop = sorted(self.pop, key = lambda s : s.f)
    #     selected = deepcopy(self.pop[:selectionNo])
        
    #     return selected

    def iterate(self):
        if self.inited == False:
            raise RuntimeWarning("Population is not initialised")
        elif self.iterNo > self.iterationMax:
            raise RuntimeWarning("Iteration limit reached")
        
        self.pop = sorted(self.pop, key = lambda s : s.f)
        offspring = deepcopy(self.pop[:self.keepBest]) # Elitism

        matingPool = self.selection()
        while len(offspring) < self.popSize:
            i = random.randint(0, len(matingPool) - 1)
            j = random.choice([j for j in range(len(matingPool)) if j != i])
            offspring.append(matingPool[i].crossover(matingPool[j]))
            
            if random.uniform(0, 1) < self.mutationRate:
                offspring[-1].mutate()
            
            if set(offspring[-1].perm) != set(range(1, self.cityNo)):
                print(offspring[-1].perm)
                raise Exception("OH SHIT OH FUCK")
        
        self.pop = deepcopy(offspring)
        self.iterNo += 1
