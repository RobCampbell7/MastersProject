import pandas as pd
import plotly.express as px

# plots a reduced objective file saved earlier, two mds axes against generation
df = pd.read_csv("reducedObj3.csv")
# df = pd.DataFrame(data)

fig = px.scatter_3d(df, x="f1", y="f2", z="Iteration")
fig.update_traces(marker_size=3, opacity=1)
# fig.update_layout(yaxis_range=[0,max(data["f2"])])
# fig.update_layout(xaxis_range=[0,max(data["f1"])])
fig.show()