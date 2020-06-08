import numpy as np
import json
import mpl_scatter_density
import matplotlib.pyplot as plt

# Generate fake data

N = 10000000
x = np.random.normal(4, 2, N)
y = np.random.normal(3, 1, N)

# Make the plot - note that for the projection option to work, the
# mpl_scatter_density module has to be imported above.
with open('../test_reported/3a084a8b-87bb-4c0c-ae6f-9bf27bdccb2c.ustracklets.1545344288529.json', 'r') as f:
    data = json.load(f)['data']

for tracklet in data:
    x = tracklet['x']
    y = tracklet['y']
    t = np.arange(len(x))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plot = ax.scatter(x, y, c = t)
    fig.colorbar(plot, ax=ax)
plt.show()
