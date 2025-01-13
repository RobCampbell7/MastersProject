import plotly.express as px

fig = px.scatter_3d(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16], z=[0, 1, 2, 3, 4])
fig.show()
