from pymoo.problems import get_problem
from pymoo.util.plotting import plot
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.scatter import Scatter
from sklearn.manifold import MDS
import matplotlib.pyplot as plt

ref_dirs = get_reference_directions("das-dennis", 5, n_partitions=12)

# known 5 objective pareto front from pymoo, squashed down with mds to see what a front looks like in fewer dimensions
pf = get_problem("dtlz3", n_obj=5).pareto_front(ref_dirs)
print(pf)
mds = MDS(n_components=3, random_state=0, normalized_stress="auto") 
  
# Fit the data to the MDS 
# object and transform the data 
X_transformed = mds.fit_transform(pf)
print(X_transformed)
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
xs = []
ys = []
zs = []
for i in range(len(X_transformed)):
    xs.append(X_transformed[i][0])
    ys.append(X_transformed[i][1])
    zs.append(X_transformed[i][2])

ax.scatter(xs, ys, zs)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

