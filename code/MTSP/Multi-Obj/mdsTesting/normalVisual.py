
from matplotlib import pyplot as plt
import numpy as np 
from sklearn.manifold import MDS 
# Generate some random data with 
# 10 dimensions and 100 samples 
x = np.random.normal(0.0, 1.0, size = (1000, 4))
mds = MDS(n_components=2, random_state=0, normalized_stress="auto") 
  
# Fit the data to the MDS 
# object and transform the data 
X_transformed = mds.fit_transform(x)

xs = []
ys = []
for i in range(len(X_transformed)):
    xs.append(X_transformed[i][0])
    ys.append(X_transformed[i][1])

fig = plt.figure()
plt.plot(xs, ys, ".")
plt.show()