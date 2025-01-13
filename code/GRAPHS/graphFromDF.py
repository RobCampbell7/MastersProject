import plotly.express as px
import plotly.io as pio
import pandas as pd

filename = "3d30c05m"

df = pd.read_csv(filename + ".csv")

fig = px.scatter_3d(df, x="PC1", y="PC2", z="Iteration", color="maxF")
fig.update_traces(marker_size=2.5, opacity=1)
fig.update_layout(width=1200, height = 1200)

print("creating images of plots")
fig.update_layout(scene_camera_eye=dict(x=0.0, y=2.0, z=0.1))
pio.write_image(fig, filename + '1p.png', scale=5, width=800, height=600)
fig.update_layout(scene_camera_eye=dict(x=2.0, y=0.1, z=0.1))
pio.write_image(fig, filename + '2p.png', scale=5, width=800, height=600)
fig.update_layout(scene_camera_eye=dict(x=0.0, y=0.0, z=2.0))
pio.write_image(fig, filename + '3p.png', scale=5, width=800, height=600)
fig.update_layout(scene_camera_eye=dict(x=2.0, y=-2.0, z=0.1))
pio.write_image(fig, filename + '4p.png', scale=5, width=800, height=600)
print("images of plot created")
fig.show()