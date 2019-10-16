import sys

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import multiprocessing

from Algorithms import BlindSearch, HillClimb, Annealing
from Functions import DeSong, Ackleyr, Griewank, Rosenbrock, Rastrigin, Schwefel, Zakharov, Michalewicz, Levy, Cos
from Utils import Plot


def plot(args):
    i, f = args
    #Plot(i + 1, f, 1000, BlindSearch, 100)
    Plot(i + 1, f, 1000, Annealing, 10)
    Plot(i + 1, f, 1000, HillClimb, 100)
    plt.show()


def main():
    functions = [
        DeSong(),
        Ackleyr(),#.SetRange(-5, 5),
        Griewank().SetRange(-5, 5),
        Rosenbrock().SetRange(-10, 10),
        Rastrigin(),
        Schwefel(),
        Zakharov().SetRange(-10, 10),
        Michalewicz().SetRange(0, 4),
        Levy().SetRange(-10, 10),
        Cos()
    ]

    pool = multiprocessing.Pool()
    pool.map(plot, zip(list(range(0, len(functions))), functions))


if __name__ == '__main__':
    main()
