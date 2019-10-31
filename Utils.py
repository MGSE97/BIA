import numpy as np

from Models import GraphData


def FullFunction(function, detail):
    step = (function.Range[1] - function.Range[0]) / detail
    x = np.arange(function.Range[0], function.Range[1], step)
    y = np.arange(function.Range[0], function.Range[1], step)
    x, y = np.meshgrid(x, y)
    z = function.Value([x, y])

    return GraphData(x, y, z)


