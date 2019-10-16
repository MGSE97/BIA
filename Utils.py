import sys

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.animation import FuncAnimation

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

def UpdatePlot(frame, algorithm, function, ax, search):
    search.append(algorithm(function, ax))

    #return [ax.zaxis, ax.xaxis, ax.yaxis]


def Plot(id, function, detail, algorithm, samples):
    name = str(id) + ': ' + type(function).__name__ + " (" + algorithm.__name__ + ")"
    print(name, ":\t\t\tComputing...")
    fig = plt.figure(name)
    fig.suptitle(name)
    ax = fig.gca(projection='3d')
    fig.canvas.draw_idle()

    # Plot the surface.
    full = FullFunction(function, detail)
    surf = ax.plot_surface(full.X, full.Y, full.Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.5)
    plt.pause(0.001)

    # Make data.
    #search = []
    #FuncAnimation(fig, UpdatePlot, fargs=[algorithm, function, ax, search], interval=100, repeat=False, frames=np.linspace(0, samples))
    search = [algorithm(function, fig, ax) for x in range(0, samples)]

    smin = GraphData(sys.maxsize, sys.maxsize, sys.maxsize)
    smax = GraphData(-sys.maxsize, -sys.maxsize, -sys.maxsize)
    points = []
    for result in search:
        points.append(result)
        if smin.Z >= result.Z:
            smin = result
        if smax.Z < result.Z:
            smax = result

    for point in points:
        color = "#000000"
        alpha = 0.6
        if point.Z == smax.Z:
            color = "#0000FF"
            alpha = 1.0
        if point.Z == smin.Z:
            color = "#FF0000"
            alpha = 1.0
        ax.scatter(point.X, point.Y, point.Z, c=color, alpha=alpha)

    print(name, ":\t\t\tMinimum [", smin.X, ", ", smin.Y, "] = ", smin.Z)
    print(name, ":\t\t\tMaximum [", smax.X, ", ", smax.Y, "] = ", smax.Z)

    # Customize the z axis.
    # ax.set_zlim(data.Min, data.Max)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)