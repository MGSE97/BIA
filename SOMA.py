import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

Axes3D = Axes3D  # pycharm auto import
from Models import GraphData
from Utils import FullFunction

NP = 20
D = 3
PRT = 1


def plot_soma(function, detail=1000):
    MIN_DIV = (function.Range[1] - function.Range[0]) / detail

    # Setup
    random.seed()
    plt.ion()
    args = []
    for d in range(0, D-1):
        args.append(np.random.uniform(function.Range[0], function.Range[1], NP))

    population = []
    for i in range(0, NP):
        p = []
        for d in range(0, D-1):
            p.append(args[d][i])
        p.append(function.Value(p))
        population.append(GraphData(p))

    fig = plt.figure("DE")
    fig.suptitle("DE")
    ax = fig.gca(projection='3d')
    fig.canvas.draw_idle()

    # Plot the surface.
    full = FullFunction(function, detail)
    surf = ax.plot_surface(full.X, full.Y, full.Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.5)
    plt.pause(0.001)

    points = []
    new_population = []
    i = 0
    while True:
        i += 1
        print(i)

        # Draw population

        for point in points:
            point.remove()
        points.clear()

        px, py, pz = [[p.X for p in population], [p.Y for p in population], [p.Z for p in population]]
        points.append(ax.plot(px, py, pz, 'ro', color='black')[0])
        plt.pause(0.01)

    plt.show()

