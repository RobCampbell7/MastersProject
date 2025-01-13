
import numpy as np 
from sklearn.manifold import MDS 
# Generate some random data with 
# 10 dimensions and 100 samples 
X = np.random.randn(100, 10) 
mds = MDS(n_components=3, random_state=0, normalized_stress="auto") 
  
# Fit the data to the MDS 
# object and transform the data 
X_transformed = mds.fit_transform(X)
print(X_transformed)