import sys

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

class GraphData:
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z


def FullFunction(function, detail):
    step = (function.Range[1] - function.Range[0]) / detail
    x = np.arange(function.Range[0], function.Range[1], step)
    y = np.arange(function.Range[0], function.Range[1], step)
    x, y = np.meshgrid(x, y)
    z = function.Value([x, y])

    return GraphData(x, y, z)


def Plot(id, function, detail, algorithm, samples):
    name = str(id) + ': ' + type(function).__name__ + " (" + algorithm.__name__ + ")"
    fig = plt.figure(name)
    fig.suptitle(name)
    ax = fig.gca(projection='3d')

    # Make data.
    search = [algorithm(function) for x in range(0, samples)]
    full = FullFunction(function, detail)

    # Plot the surface.
    surf = ax.plot_surface(full.X, full.Y, full.Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.5)

    smin = GraphData(sys.maxsize, sys.maxsize, sys.maxsize)
    smax = GraphData(-sys.maxsize, -sys.maxsize, -sys.maxsize)
    for result in search:
        if smin.Z >= result.Z:
            smin = result
        if smax.Z < result.Z:
            smax = result
        ax.scatter(result.X, result.Y, result.Z, c="#000000")

    print(name, ":\t\t\tMinimum [", smin.X, ", ", smin.Y, "] = ", smin.Z)
    print(name, ":\t\t\tMaximum [", smax.X, ", ", smax.Y, "] = ", smax.Z)

    # Customize the z axis.
    # ax.set_zlim(data.Min, data.Max)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)