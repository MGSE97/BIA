import random
from itertools import product
import matplotlib.lines as mlines

from Utils import GraphData


def BlindSearch(function, ax):
    x = random.uniform(function.Range[0], function.Range[1])
    y = random.uniform(function.Range[0], function.Range[1])
    return GraphData(x, y, function.Value([x, y]))

def HillClimb(function, ax):
    r = (function.Range[1] - function.Range[0]) / 100.0
    x = random.uniform(function.Range[0]+r, function.Range[1]-r)
    y = random.uniform(function.Range[0]+r, function.Range[1]-r)
    z = function.Value([x, y])
    xs = []
    ys = []
    zs = []
    t = 10
    while t > 0:
        px = [x-r, x, x+r]
        py = [y-r, y, y-r]
        for i, j in product(px, py):
            if i < function.Range[0] or i > function.Range[1]:
                continue
            if j < function.Range[0] or j > function.Range[1]:
                continue
            if i == x and j == y:
                continue
            l = function.Value([i, j])
            if l < z:
                t = 10
                z = l
                x = i
                y = j
                xs.append(x)
                ys.append(y)
                zs.append(z)
        t -= 1

    ax.plot(xs, ys, zs)

    return GraphData(x, y, z)

