import pandas as pd
import plotly.express as px

df = pd.read_csv("reducedObj.csv")
# df = pd.DataFrame(data)

fig = px.scatter_3d(df, x="PC1", y="PC2", z="Iteration", color="maxF")
fig.update_traces(marker_size=3, opacity=1)
# fig.update_layout(yaxis_range=[0,max(data["f2"])])
# fig.update_layout(xaxis_range=[0,max(data["f1"])])
fig.show()