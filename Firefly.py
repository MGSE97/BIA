import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

Axes3D = Axes3D  # pycharm auto import
from Models import Firefly, Vector
from Utils import FullFunction

NP = 20
D = 3
Alpha = 0.5
Beta = 1.0
Gama = 0.2
Gama2 = 0.01
Omega = 1.0


def vector_rand():
    return Vector(np.random.uniform(-1, 1, D-1))


def plot_fireflies(function, detail = 1000):
    # Setup
    random.seed()
    plt.ion()

    # Create population
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
        f = Firefly(p)
        population.append(f)

    # Set plots
    fig = plt.figure("Firefly")
    fig.suptitle("Firefly")
    ax = fig.gca(projection='3d')
    fig.canvas.draw_idle()

    # Plot the surface.
    full = FullFunction(function, detail)
    surf = ax.plot_surface(full.X, full.Y, full.Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.5)
    plt.pause(0.001)

    points = []
    g = 0
    best = population[0].copy()
    while True:
        g += 1
        print(g, best)

        # Draw population
        for point in points:
            point.remove()
        points.clear()

        # Move best
        direction = function.FixRange((best + Alpha*vector_rand()).Data)
        direction.append(function.Value(direction))
        best.set(direction)

        # Move population
        for i in population:
            if i == best:
                continue

            for j in population:
                if j.brightness() < i.brightness():
                    #move fly
                    #direction = Beta * np.exp(-Gama2 * i.distance(j)**2) * (j - i) + Alpha * vector_rand()
                    #direction = Beta*np.exp(-Gama*i.distance(j))*(j - i) + Alpha*vector_rand()
                    direction = Beta * (1.0/(Omega + i.distance(j))) * (j - i) + Alpha * vector_rand()
                    firefly = function.FixRange((i + direction).Data)
                    firefly.append(function.Value(firefly))
                    i.set(firefly)

        # Find Best
        for i in population:
            if i.brightness() < best.brightness():
                best = i.copy()

        px, py, pz = [[p.X for p in population], [p.Y for p in population], [p.Z for p in population]]
        points.append(ax.plot(px, py, pz, 'ro', color='black', alpha=0.5)[0])
        points.append(ax.plot([best.X], [best.Y], [best.Z], 'ro', color='red')[0])
        plt.pause(0.01)

    plt.show()
