import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
Axes3D = Axes3D  # pycharm auto import
from Models import GraphData
from Utils import FullFunction


def plot_diff_evolution(function, detail=1000):
    step = (function.Range[1] - function.Range[0])/100.0
    population = [GraphData(
        np.arange(function.Range[0], function.Range[1], step),
        np.arange(function.Range[0], function.Range[1], step),
        np.arange(function.Range[0], function.Range[1], step)
    ) for x in range(0, 20)]

    fig = plt.figure("DE")
    fig.suptitle("DE")
    ax = fig.gca(projection='3d')
    fig.canvas.draw_idle()


    # Plot the surface.
    full = FullFunction(function, detail)
    surf = ax.plot_surface(full.X, full.Y, full.Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.5)
    plt.pause(0.001)

    for point in population:
        ax.scatter(point.X, point.Y, point.Z, c='black', alpha=0.5)

