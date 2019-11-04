import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

Axes3D = Axes3D  # pycharm auto import
from Models import GraphData
from Utils import FullFunction

F = GraphData(0.5, 0.5, 0.5)
CR = 0.2
NP = 20
D = 3


# best
def mutate(a, b, c):
    return GraphData((a + F * (b - c)).Data)


# binomial
def cross(function, x, y):
    # Get random index
    r = random.randrange(0, D-1)
    # Generate indexes
    rs = [np.random.random() for d in range(0, D-1)]
    # Set values
    z = []
    for i, ri in enumerate(rs):
        if ri < CR or i == r:
            z.append(y.Data[i])
        else:
            z.append(x.Data[i])

    z.append(function.Value(x.Data))
    return GraphData(z)


def evaluate(a, b):
    return a.Data[D - 1] > b.Data[D - 1]


def fix_mutation(function, y):
    r = []
    for x in y.Data:
        if function.Range[0] <= x <= function.Range[1]:
            r.append(x)
        else:
            r.append(np.random.uniform(function.Range[0], function.Range[1], 1)[0])
    return GraphData(r)


def plot_diff_evolution(function, detail=1000):
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
    for point in population:
        points.append(ax.scatter(point.X, point.Y, point.Z, c='black', alpha=0.5))

    new_population = []
    p = 0
    while True:
        p += 1
        print(p, len(population))
        plt.pause(0.001)
        # Compute
        for x in population:
            # Get 3 from population
            samples = random.sample(population, k=3)
            # Compute temp vector
            y = mutate(samples[0], samples[1], samples[2])
            y = fix_mutation(function, y)
            # Cross selected
            y = cross(function, x, y)
            # Select new population
            if evaluate(x, y):
                new_population.append(y)
            else:
                new_population.append(x)

        # Draw population
        for i, point in enumerate(population):
            #points[i].set_offsets(np.c_[point.X, point.Y, point.Z])
            #points[i].set_value(point.Z)
            #points[i].set_xdata([point.X])
            #points[i].set_ydata([point.Y])
            #points[i].set_zdata([point.Z])
            ax.scatter(point.X, point.Y, point.Z, c='black', alpha=0.5)

        population.clear()
        population.extend(new_population)
        new_population.clear()

    plt.show()
