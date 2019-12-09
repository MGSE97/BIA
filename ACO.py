from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

Axes3D = Axes3D  # pycharm auto import
from Models import GraphData, Vector, Member, City, Ant, CityACO
from Utils import FullFunction

NC = 20
D = 3
MIN = 0
MAX = 100
Alpha = 1
Beta = 2
Evaporation = 0.9


def create_city(name):
    return CityACO(name, np.random.uniform(MIN, MAX, D - 1))


def create_ant(x, cities):
    return Ant(str(x), random.sample(cities, 1)[0], cities)


def possibilityToVisit(ant, cities, alpha, beta):
    # calculate probability to visit each new city
    posibilityToVisit = []
    s = 0
    for c in cities:
        if ant.City.Name == c.Name or ant.Origin.Name == c.Name:
            continue
        d = ant.City.getDistance(c)
        if d is None:
            continue
        v = True
        for r, t in ant.Route:
            if r.Name == c.Name:
                v = False
                break
        if v:
            p = d.Pheromons ** alpha * d.Visibility ** beta
            posibilityToVisit.append([c, p])
            s += p

    if s > 0:
        for i, v in enumerate(posibilityToVisit):
            posibilityToVisit[i][1] = v[1] / s + (posibilityToVisit[i - 1][1] if i > 0 else 0)
            #posibilityToVisit[i][1] = v[1] / s

    return posibilityToVisit


def evaporate(cities):
    for c in cities:
        for n, d in c.Distances.items():
            d.Pheromons *= Evaporation


def plot_path(t, r):
    tx = [city.X for city, distance in r]
    ty = [city.Y for city, distance in r]
    t.set_xdata(tx)
    t.set_ydata(ty)


def plot_aco():
    cities = [create_city(str(chr(65 + x))) for x in range(0, NC)]
    ants = [create_ant(x, cities) for x in range(0, 2 * NC)]

    fig = plt.figure('Cities ACO')
    fig.suptitle('Cities ACO')
    ax = fig.gca()
    fig.canvas.draw_idle()

    for c in cities:
        c.updateDistances(cities)
        ax.plot(c.X, c.Y, marker='v')
        ax.annotate(c.Name, (c.X - len(c.Name) / 2 - 0.25, c.Y + 2))
        #print(str(c) + '\n\n')

    plt.pause(0.00001)

    fstats = plt.figure('Ants')
    fstats.suptitle('Best routes')
    fax = fstats.gca()
    fax.set_xlim(0, 1000)
    fax.set_ylim(0, 1200)
    fstats.canvas.draw_idle()

    e = 0
    sp = 10
    max_distance = 0
    current_distance = []
    populations = []
    distances = []

    sc, = fax.plot(current_distance, populations, alpha=0.25)
    sb, = fax.plot(distances, populations)

    t, = ax.plot([], [], alpha=0.25)
    b, = ax.plot([], [], alpha=0.5)

    best = None
    bestPath = []
    while True:
        print(e, best)
        # move ants
        c = len(cities)
        while c > 0:
            for ant in ants:
                p = random.random()
                possibilities = possibilityToVisit(ant, cities, Alpha, Beta)
                if len(possibilities) == 0:
                    ant.visitedCity(ant.Origin)
                    c -= 1
                else:
                    for i, pos in enumerate(possibilities):
                        if p < pos[1]:
                            ant.visitedCity(pos[0])
                            break

        # get best
        distance = max_distance
        for ant in ants:
            if ant.Distance > max_distance:
                max_distance = ant.Distance
            if ant.Distance < distance:
                distance = ant.Distance
            if best is None or ant.Distance < best:
                fig.suptitle(ant.str())
                best = ant.Distance
                bestPath = ant.Route.copy()
                plot_path(b, bestPath)

        # draw ants
        current_distance.append(distance)
        populations.append(e)
        distances.append(best)
        if e % sp == 1:
            sb.set_xdata(populations)
            sb.set_ydata(distances)
            sc.set_xdata(populations)
            sc.set_ydata(current_distance)

            # Draw route
            plot_path(t, bestPath)
            plt.pause(0.0000001)

            # Evolve population
            fax.set_xlim(0, e)
            fax.set_ylim(0, max_distance)
            if e > 1000:
                sp = 50

        plt.pause(0.00001)

        # evaporate
        evaporate(cities)

        # reset ants
        for ant in ants:
            ant.reset(cities)
        e += 1

    plt.show()
