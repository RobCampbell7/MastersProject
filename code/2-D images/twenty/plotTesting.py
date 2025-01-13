import plotly.express as px
import plotly.io as pio
import pandas as pd

df = pd.read_csv("./simple.csv")
paretodf = pd.read_csv("./pareto.csv")

fig1 = px.scatter_3d(df, x="F1", y="F2", z="Iteration")
fig1.update_traces(marker_size=2.5, opacity=0.9)
fig1.update_layout(width=1200, height = 1200)
print("Figure 1 created")
fig1.update_layout(scene_camera_eye=dict(x=0.0, y=2.0, z=0.1))
pio.write_image(fig1, 'simpleImage1.png', scale=4, width=600, height=600)
print("First image saved")
fig1.update_layout(scene_camera_eye=dict(x=2.0, y=0.1, z=0.1))
pio.write_image(fig1, 'simpleImage2.png', scale=4, width=600, height=600)
print("Second image saved")
fig1.update_layout(scene_camera_eye=dict(x=0.0, y=0.0, z=2.0))
pio.write_image(fig1, 'simpleImage3.png', scale=4, width=600, height=600)
print("Third image saved")
fig1.update_layout(scene_camera_eye=dict(x=2.0, y=-2.0, z=0.1))
pio.write_image(fig1, 'simpleImage4.png', scale=4, width=600, height=600)
print("Fourth image saved")

del(fig1)

fig2 = px.scatter_3d(paretodf, x="F1", y="F2", z="Iteration")
fig2.update_traces(marker_size=2.5, opacity=0.9)
fig2.update_layout(width=1200, height = 1200)
print("\nFigure 2 created")

fig2.update_layout(scene_camera_eye=dict(x=0.0, y=2.0, z=0.1))
pio.write_image(fig2, 'paretoImage1.png',scale=4, width=600, height=600)
print("First image saved")

fig2.update_layout(scene_camera_eye=dict(x=2.0, y=0.1, z=0.1))
pio.write_image(fig2, 'paretoImage2.png',scale=4, width=600, height=600)
print("Second image saved")

fig2.update_layout(scene_camera_eye=dict(x=0.0, y=0.0, z=2.0))
pio.write_image(fig2, 'paretoImage3.png',scale=4, width=600, height=600)
print("Third image saved")

fig2.update_layout(scene_camera_eye=dict(x=2.0, y=-2.0, z=0.1))
pio.write_image(fig2, 'paretoImage4.png',scale=4, width=600, height=600)
print("Fourth image saved")
