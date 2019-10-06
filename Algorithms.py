import random

from Utils import GraphData


def BlindSearch(function):
    x = random.uniform(function.Range[0], function.Range[1])
    y = random.uniform(function.Range[0], function.Range[1])
    return GraphData(x, y, function.Value([x, y]))

