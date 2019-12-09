import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

Axes3D = Axes3D  # pycharm auto import
from Models import GraphData, Vector, Member
from Utils import FullFunction

NP = 20
D = 3

def plot_fireflies(function, detail = 1000):
    # Setup
    random.seed()
    plt.ion()
    args = []
    step = (function.Range[1] - function.Range[0]) / 100
    for d in range(0, D - 1):
        args.append(np.random.uniform(function.Range[0], function.Range[1], NP))

    population = []
    for i in range(0, NP):
        p = []
        for d in range(0, D - 1):
            p.append(args[d][i])
        p.append(function.Value(p))
        m = Member(p)
        m.Velocity = GraphData(np.random.uniform(-1, 1, NP))
        population.append(m)

    fig = plt.figure("Firefly")
    fig.suptitle("Firefly")
    ax = fig.gca(projection='3d')
    fig.canvas.draw_idle()

    # Plot the surface.
    full = FullFunction(function, detail)
    surf = ax.plot_surface(full.X, full.Y, full.Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.5)
    plt.pause(0.001)

    points = []
    i = 0
    best = population[0].Best
    while True:
        i += 1
        print(i, best)

        # Draw population
        for point in points:
            point.remove()
        points.clear()

        # Move population

        px, py, pz = [[p.X for p in population], [p.Y for p in population], [p.Z for p in population]]
        points.append(ax.plot(px, py, pz, 'ro', color='black', alpha=0.5)[0])
        points.append(ax.plot([best.X], [best.Y], [best.Z], 'ro', color='red')[0])
        plt.pause(0.01)

    plt.show()