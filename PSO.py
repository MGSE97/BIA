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
C1 = 2.0
C2 = 2.0


def plot_pso(function, detail=1000):
    # Setup
    random.seed()
    plt.ion()
    args = []
    step = (function.Range[1] - function.Range[0]) / 100
    for d in range(0, D-1):
        args.append(np.random.uniform(function.Range[0], function.Range[1], NP))

    population = []
    for i in range(0, NP):
        p = []
        for d in range(0, D-1):
            p.append(args[d][i])
        p.append(function.Value(p))
        m = Member(p)
        m.Velocity = GraphData(np.random.uniform(-1, 1, NP))
        population.append(m)

    fig = plt.figure("PSO")
    fig.suptitle("PSO")
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
        for m in population:
            best = move_member(m, best, step, function)
            points.append(ax.quiver(m.X, m.Y, m.Z, m.Velocity.X, m.Velocity.Y, m.Velocity.Z, length=step, arrow_length_ratio=0.01, alpha=0.3))

        px, py, pz = [[p.X for p in population], [p.Y for p in population], [p.Z for p in population]]
        points.append(ax.plot(px, py, pz, 'ro', color='black', alpha=0.5)[0])
        points.append(ax.plot([best.X], [best.Y], [best.Z], 'ro', color='red')[0])
        plt.pause(0.01)

    plt.show()


def vector_rand():
    return Vector(np.random.uniform(0, 1, D-1))

def move_member(m, best, step, function):
    # calc new speed
    m.Velocity = m.Velocity + C1 * vector_rand() * (m.Best - m) + C2 * vector_rand() * (best - m)
    m.Velocity = GraphData(m.Velocity.Data)
    # move member
    newPosition = m + step * m.Velocity
    newPos = []
    for i in range(0, D-1):
        if function.Range[0] > newPosition.Data[i]:
            newPos.append(function.Range[0])
        elif function.Range[1] < newPosition.Data[i]:
            newPos.append(function.Range[1])
        else:
            newPos.append(newPosition.Data[i])

    # evaluate
    newPos.append(function.Value(newPos))
    newPos = GraphData(newPos)
    if (newPos.last() <= m.Best.last()):
        m.Best = newPos
        m.set(newPos.Data)
        if (m.Best.last() <= best.last()):
            best = m.Best
    return best
