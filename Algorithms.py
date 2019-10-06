import random

def BindSearch(limit, function):
    x = random.randomrange(limit)
    return function.Value([x])