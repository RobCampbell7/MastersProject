from pymoo.problems import get_problem
from pymoo.util.plotting import plot
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.scatter import Scatter
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

ref_dirs = get_reference_directions("das-dennis", 5, n_partitions=12)

pf = get_problem("dtlz4").pareto_front(ref_dirs)
print(pf)
mds = MDS(n_components=2, random_state=0, normalized_stress="auto") 
  
# Fit the data to the MDS 
# object and transform the data 
X_transformed = mds.fit_transform(pf)
# print(X_transformed)
# X_transformed = pf
fig = plt.figure()
ax = fig.add_subplot()


# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
xs = []
ys = []
for i in range(len(X_transformed)):
    xs.append(X_transformed[i][0])
    ys.append(X_transformed[i][1])

ax.scatter(xs, ys)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')

plt.show()

