
from random import uniform
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.manifold import MDS

# Generate some random data with 
# 10 dimensions and 100 samples 
X = np.array([[uniform(-100, 100) for i in range(10)] for i in range(400)])
mds = MDS(n_components=3, random_state=0, normalized_stress="auto") 
  
# Fit the data to the MDS 
# object and transform the data 
X_transformed = mds.fit_transform(X)

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