import numpy as np
from pymoo.core.repair import Repair
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.optimize import minimize
from pymoo.problems.single.traveling_salesman import create_random_tsp_problem
from pymoo.operators.sampling.rnd import PermutationRandomSampling
from pymoo.operators.crossover.erx import EdgeRecombinationCrossover
from pymoo.operators.mutation.inversion import InversionMutation
from pymoo.termination.default import DefaultSingleObjectiveTermination
from pymoo.problems.single.traveling_salesman import visualize

# single objective tsp in pymoo, kept as a comparison
class StartFromZeroRepair(Repair):

    def _do(self, problem, X, **kwargs):
        I = np.where(X == 0)[1]

        for k in range(len(X)):
            i = I[k]
            # rotate each tour so it starts at city 0, the tour itself doesn't change
            X[k] = np.concatenate([X[k, i:], X[k, :i]])

        return X

problem = create_random_tsp_problem(30, 100, 100, seed=1)

algorithm = GA(
    pop_size=200,
    sampling=PermutationRandomSampling(),
    mutation=InversionMutation(),
    crossover=EdgeRecombinationCrossover(),
    repair=StartFromZeroRepair(),
    eliminate_duplicates=True
)

# if the algorithm did not improve the last 200 generations then it will terminate (and disable the max generations)
termination = DefaultSingleObjectiveTermination(period=200, n_max_gen=np.inf)

res = minimize(
    problem,
    algorithm,
    termination,
    seed=1,
)

print("Traveling Time:", np.round(res.F[0], 3))
print("Function Evaluations:", res.algorithm.evaluator.n_eval)

visualize(problem, res.X, show=True)
input()
