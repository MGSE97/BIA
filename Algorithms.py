import random
from itertools import product
import matplotlib.lines as mlines
import numpy as np
import matplotlib.pyplot as plt

from Utils import GraphData


def BlindSearch(function, fig, ax):
    x = random.uniform(function.Range[0], function.Range[1])
    y = random.uniform(function.Range[0], function.Range[1])
    return GraphData(x, y, function.Value([x, y]))


def HillClimb(function, fig, ax):
    w = (function.Range[1] - function.Range[0]) * 0.01
    s = w * 0.1
    x = random.uniform(function.Range[0]+w, function.Range[1]-w)
    y = random.uniform(function.Range[0]+w, function.Range[1]-w)
    z = function.Value([x, y])
    xs = []
    ys = []
    zs = []
    t = 10
    while t > 0:
        for sx in np.arange(x-w, x+w, s):
            for sy in np.arange(y-w, y+w, s):
                if sx < function.Range[0] or sx > function.Range[1]:
                    continue
                if sy < function.Range[0] or sy > function.Range[1]:
                    continue
                if x + s >= sx >= x - s and y + s >= sy >= y - s:
                    continue
                sz = function.Value([sx, sy])
                if sz < z:
                    t = 10
                    z = sz
                    x = sx
                    y = sy
        xs.append(x)
        ys.append(y)
        zs.append(z)
        t -= 1

    ax.plot(xs, ys, zs)
    fig.canvas.draw()
    fig.canvas.flush_events()

    return GraphData(x, y, z)


def Annealing(function, fig, ax):
    w = (function.Range[1] - function.Range[0]) * 0.01
    s = w * 0.1
    x = random.uniform(function.Range[0]+w, function.Range[1]-w)
    y = random.uniform(function.Range[0]+w, function.Range[1]-w)
    z = function.Value([x, y])
    xs = []
    ys = []
    zs = []
    temperature = 200.0
    heating = 0.9
    while temperature > 0.1:
        i = 10
        while i > 0:
            sx = random.uniform(x-w, x+w)
            sy = random.uniform(y-w, y+w)
            if sx < function.Range[0] or sx > function.Range[1]:
                continue
            if sy < function.Range[0] or sy > function.Range[1]:
                continue
            if x + s >= sx >= x - s and y + s >= sy >= y - s:
                continue
            sz = function.Value([sx, sy])
            if sz < z:
                z = sz
                x = sx
                y = sy
            else:
                probability = np.exp(-(sz - z) / temperature)
                if random.uniform(0, 1.0) < probability:
                    z = sz
                    x = sx
                    y = sy
            i -= 1

        xs.append(x)
        ys.append(y)
        zs.append(z)
        temperature *= heating

    ax.plot(xs, ys, zs)
    fig.canvas.draw()
    fig.canvas.flush_events()

    return GraphData(x, y, z)


