import multiprocessing

from mpl_toolkits.mplot3d import Axes3D
Axes3D = Axes3D  # pycharm auto import
from matplotlib import cm
import matplotlib.pyplot as plt
import sys

from matplotlib.ticker import LinearLocator, FormatStrFormatter

from Algorithms import Annealing, HillClimb
from Models import GraphData
from Utils import FullFunction

from Functions import DeSong, Ackleyr, Griewank, Rosenbrock, Rastrigin, Schwefel, Zakharov, Michalewicz, Levy, Cos

def plot(args):
    i, f = args
    #Plot(i + 1, f, 1000, BlindSearch, 100)
    Plot(i + 1, f, 1000, Annealing, 10)
    Plot(i + 1, f, 1000, HillClimb, 10)
    plt.show()


def plot_functions():
    functions = [
        # DeSong(),
        # Ackleyr(),  # .SetRange(-5, 5),
        # Griewank().SetRange(-5, 5),
        # Rosenbrock().SetRange(-10, 10),
        # Rastrigin(),
        # Schwefel(),
        Zakharov().SetRange(-10, 10),
        # Michalewicz().SetRange(0, 4),
        # Levy().SetRange(-10, 10),
        Cos()
    ]

    pool = multiprocessing.Pool(len(functions))
    pool.map(plot, zip(list(range(0, len(functions))), functions))


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


