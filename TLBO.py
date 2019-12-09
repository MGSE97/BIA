import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

Axes3D = Axes3D  # pycharm auto import
from Models import Vector, GraphData
from Utils import FullFunction

NP = 20
D = 3


def vector_rand():
    return Vector(np.random.uniform(0, 1, D-1))


def plot_tlbo(function, detail = 1000):
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
        f = GraphData(p)
        population.append(f)

    # Set plots
    fig = plt.figure("TLBO")
    fig.suptitle("TLBO")
    ax = fig.gca(projection='3d')
    fig.canvas.draw_idle()

    # Plot the surface.
    full = FullFunction(function, detail)
    surf = ax.plot_surface(full.X, full.Y, full.Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.5)
    plt.pause(0.001)

    points = []
    g = 0
    teacher = population[0].copy()
    while True:
        g += 1
        print(g, teacher)

        # Draw population
        for point in points:
            point.remove()
        points.clear()

        px, py, pz = [[p.X for p in population], [p.Y for p in population], [p.Z for p in population]]
        points.append(ax.plot(px, py, pz, 'ro', color='black', alpha=0.5)[0])
        points.append(ax.plot([teacher.X], [teacher.Y], [teacher.Z], 'ro', color='red')[0])
        plt.pause(0.01)

        # Find best teacher
        x_mean = Vector([0,0,0])
        for m in population:
            if m.last() < teacher.last():
                teacher = m.copy()
            x_mean += m

        x_mean = 1.0/len(population) * x_mean
        Tf = np.round(np.random.uniform(1, 2))
        
        # Teach
        newPopulation = []
        for m in population:
            if m is teacher:
                continue
            
            pos = function.FixRange((m + vector_rand() * (teacher - Tf * x_mean)).Data)
            pos.append(function.Value(pos))
            pos = GraphData(pos)
            if pos.last() < m.last():
                newPopulation.append(pos)
            else:
                newPopulation.append(m)

        # Learn
        for m in newPopulation:
            l = random.sample(newPopulation, k=1)[0]
            while m is l:
                l = random.sample(newPopulation, k=1)[0]

            pos = function.FixRange((m + vector_rand() * ((m - l) if m.last() <= l.last() else (l - m))).Data)
            pos.append(function.Value(pos))
            if pos[len(pos) - 1] < m.last():
                m.set(pos)

        population = newPopulation

    plt.show()
