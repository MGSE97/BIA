import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from Algorithms import AnnealingSingle, HillClimbSingle

Axes3D = Axes3D  # pycharm auto import
from Models import GraphData, Vector
from Utils import FullFunction

NP = 20
D = 3
PATH_LENGTH = 5
STEP = 0.11
PRT = 0.5


def plot_soma(function, detail=1000):
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

    fig = plt.figure("SOMA")
    fig.suptitle("SOMA")
    ax = fig.gca(projection='3d')
    fig.canvas.draw_idle()

    # Plot the surface.
    full = FullFunction(function, detail)
    surf = ax.plot_surface(full.X, full.Y, full.Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.5)
    plt.pause(0.001)

    points = []
    i = 0
    while True:
        i += 1
        print(i, len(population))

        # Draw population
        for point in points:
            point.remove()
        points.clear()

        px, py, pz = [[p.X for p in population], [p.Y for p in population], [p.Z for p in population]]
        points.append(ax.plot(px, py, pz, 'ro', color='black')[0])
        plt.pause(0.01)

        leader = find_leader(population)
        leader = move_leader(function, leader)

        population = move_others(function, population, leader, STEP)

    plt.show()


def find_leader(population):
    best = population[0]
    for member in population:
        if member.last() < best.last():
            best = member

    return best


def move_leader(function, leader):
    #return AnnealingSingle(function, leader)
    return HillClimbSingle(function, leader)


def move_others(function, population, leader, step):
    newPopulation = []
    newPopulation.append(leader)

    leaderIndex = population.index(leader)
    for i, member in enumerate(population):
        if i == leaderIndex:
            continue

        pertubatingVector = []
        for d in range(0, D - 1):
            r = random.random()
            pertubatingVector.append(0 if r <= PRT else 1)

        pertubatingVector = Vector(pertubatingVector)

        newMember = member
        t = step
        while t < PATH_LENGTH:

            # D-1
            vector = member + (member - leader) * t * pertubatingVector
            data = []
            for v in vector.Data:
                if v < function.Range[0] or v > function.Range[1]:
                    data.append(np.random.uniform(function.Range[0], function.Range[1], 1)[0])
                else:
                    data.append(v)
            data.append(function.Value(data))
            vector = GraphData(data)

            if vector.last() <= newMember.last():
                newMember = vector

            t += step

        newPopulation.append(newMember)

    return newPopulation


