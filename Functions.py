import math
import numpy as np


class DeSong:
    Range = [-5.12, 5.12]

    @staticmethod
    def Value(x):
        return np.sum([np.pow(x, 2) for x in x])

class Ackleyr:
    Range = [-32.768, 32.768]
    A = 20
    B = 0.2
    C = 2*np.pi

    @staticmethod
    def Value(x):
        return -Ackleyr.A * math.exp(-Ackleyr.B * math.sqrt( sum([pow(x,2) for x in x])/len(x) )) - \
               math.exp( sum([Ackleyr.C*x for x in x])/len(x) ) + \
               math.exp(1)

class DeSong:
    Range = [-5.12, 5.12]

    @staticmethod
    def Value(x):
        return sum([pow(x, 2) for x in x])
