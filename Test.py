from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import itertools
from Functions import DeSong

fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X = np.arange(DeSong.Range[0], DeSong.Range[1], 0.1)
Y = np.arange(DeSong.Range[0], DeSong.Range[1], 0.1)
X, Y = np.meshgrid(X, Y)
Z = DeSong.Value([X, Y])
#for x, y in itertools.product(X, Y):
 #   Z.append(DeSong.Value([x, y]))

# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# Customize the z axis.
ax.set_zlim(DeSong.Range[0]*2, DeSong.Range[1]*2)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
