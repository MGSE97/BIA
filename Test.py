import random
import sys

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import multiprocessing

from Algorithms import BlindSearch, HillClimb, Annealing
from Functions import DeSong, Ackleyr, Griewank, Rosenbrock, Rastrigin, Schwefel, Zakharov, Michalewicz, Levy, Cos
from Models import City
from Utils import Plot, send_traveler, plot_cities


def plot(args):
    i, f = args
    #Plot(i + 1, f, 1000, BlindSearch, 100)
    Plot(i + 1, f, 1000, Annealing, 10)
    Plot(i + 1, f, 1000, HillClimb, 10)
    plt.show()


def cities(args):
    i, f = args


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


def main():
    # plot_functions()
    plot_cities()


if __name__ == '__main__':
    main()
