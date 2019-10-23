import random
import sys

import numpy
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.animation import FuncAnimation

from Models import GraphData, Traveler, City


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


travelers = ["Horo", "Leny", "Carl", "Lawrence", "Chloe", "Nora", "Ruby"]


def send_traveler(cities):
    traveler = Traveler(
        travelers[random.randrange(0, len(travelers))],
        cities[random.randrange(0, len(cities))]
    )

    traveler.route(cities)

    return traveler


def send_population(population, cities, count):
    traveler = None
    for i in range(0, count):
        t = send_traveler(cities)
        if traveler is None or t.Distance < traveler.Distance:
            traveler = t
    return traveler

def plot_cities():
    cities = [City(str(chr(65+i)), random.randrange(0, 100), random.randrange(0, 100)) for i in range(0, 20)]
    fig = plt.figure('Cities')
    fig.suptitle('Cities')
    ax = fig.gca()
    fig.canvas.draw_idle()

    for c in cities:
        c.updateDistances(cities)
        ax.plot(c.X, c.Y, marker='v')
        ax.annotate(c.Name, (c.X-len(c.Name)/2-0.25, c.Y+2))
        print(str(c)+'\n\n')

    a = cities[random.randrange(0, 10)]
    b = cities[random.randrange(10, 20)]

    print(str(a) + '\n' + str(b) + '\n = ' + str(a.getDistance(b)))

    plt.pause(0.00001)

    fstats = plt.figure('Travelers')
    fstats.suptitle('Best routes')
    fax = fstats.gca()
    fax.set_xlim(0, 1000)
    fax.set_ylim(400, 1200)
    fstats.canvas.draw_idle()

    distances = []
    populations = []
    currentd = []
    sc, = fax.plot(currentd, populations, alpha=0.25)
    s, = fax.plot(distances, populations)
    best = None

    population = []
    t, = ax.plot([], [], alpha=0.25)
    b, = ax.plot([], [], alpha=0.5)
    for i in range(0, 1000):
        # Get best route from population
        traveler = send_population(population, cities, 10)
        print(traveler.str())

        # Update global best
        if best is None or best.Distance >= traveler.Distance:
            fig.suptitle(traveler.str())
            best = traveler
            plot_path(b, traveler)

        # Draw stats
        currentd.append(traveler.Distance)
        populations.append(i)
        distances.append(best.Distance)
        s.set_xdata(populations)
        s.set_ydata(distances)
        sc.set_xdata(populations)
        sc.set_ydata(currentd)

        # Draw route
        plot_path(t, traveler)
        plt.pause(0.00001)

    plt.show()


def plot_path(t, traveler):
    tx = [city.X for city, distance in traveler.Route]
    ty = [city.Y for city, distance in traveler.Route]
    t.set_xdata(tx)
    t.set_ydata(ty)

