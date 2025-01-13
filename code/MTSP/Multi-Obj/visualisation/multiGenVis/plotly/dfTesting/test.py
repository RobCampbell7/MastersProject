import pandas as pd

data = {
    "perm" : [[0, 1, 2], [0, 2, 1], [1, 0, 2]],
       "x" : [3, 4, 2],
       "y" : [2, 4, 3],
       "i" : [0, 1, 2]
}

df = pd.DataFrame(data)
for i in range(len(df)):
    print(df.loc[0])