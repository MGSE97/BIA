import numpy as np


class BaseFunction(object):

    def __init__(self):
        self.Range = [0, 0]

    def SetRange(self, rangeMin, rangeMax):
        self.Range = [rangeMin, rangeMax]
        return self

    def Value(self, x):
        pass

    pass


class DeSong(BaseFunction):

    def __init__(self):
        self.Range = [-5.12, 5.12]

    def Value(self, x):
        return sum([pow(x, 2) for x in x])


class Ackleyr(BaseFunction):

    def __init__(self):
        self.Range = [-32.768, 32.768]
        self.A = 20
        self.B = 0.2
        self.C = 0.5  # 2 * np.pi

    def Value(s, x):
        sumA = sum([pow(x, 2) for x in x]) / len(x)
        sumB = sum([np.cos(s.C * x) for x in x]) / len(x)
        return (
                    -s.A * np.exp(
                        -s.B * np.sqrt(sumA)
                    ) -
                    np.exp(sumB) +
                    s.A +
                    np.exp(1)
                )


class Griewank(BaseFunction):

    def __init__(self):
        self.Range = [-600, 600]

    def Value(self, x):
        prod = 1
        for i, v in enumerate(x):
            prod *= np.cos(v/np.sqrt(i+1))

        return sum([pow(x, 2) for x in x]) / 4000 - prod + 1


class Rosenbrock(BaseFunction):

    def __init__(self):
        self.Range = [-5, 10]

    def Value(self, x):
        result = 0
        for i, v in enumerate(x):
            if i < (len(x) - 1):
                result += 100 * pow(x[i + 1] - pow(v, 2), 2) + pow(v - 1, 2)

        return result


class Rastrigin(BaseFunction):

    def __init__(self):
       self.Range = [-5.12, 5.12]

    def Value(self, x):
        return (
            10*len(x) +
            sum([
                    pow(x, 2) -
                    10 * np.cos(2 * np.pi * x)
                for x in x]
            )
        )


class Schwefel(BaseFunction):

    def __init__(self):
        self.Range = [-500, 500]

    def Value(self, x):
        return (
            418.9829 * len(x) -
            sum([x * np.sin(np.sqrt(np.abs(x))) for x in x])
        )


class Zakharov(BaseFunction):

    def __init__(self):
        self.Range = [-5, 10]

    def Value(self, x):
        return (
            sum([pow(x, 2) for x in x]) +
            pow(sum([0.5 * (i+1) * v for i, v in enumerate(x)]), 2) +
            pow(sum([0.5 * (i+1) * v for i, v in enumerate(x)]), 4)
        )


class Michalewicz(BaseFunction):

    def __init__(self):
        self.Range = [0, np.pi]
        self.M = 10

    def Value(s, x):
        result = 0
        for i, v in enumerate(x):
            result += np.sin(v) * pow(np.sin(((i + 1) * pow(v, 2)) / np.pi), 2 * s.M)
        return -result


class Levy(BaseFunction):

    def __init__(self):
        self.Range = [-10, 10]

    def Value(s, x):
        result = 0
        for i, v in enumerate(x):
            if i < (len(x) - 1):
                result += pow(s.Wi(v) - 1, 2) * (1 + 10 * pow(np.sin(np.pi * s.Wi(v) + 1), 2))

        return (
            pow(np.sin(np.pi * s.Wi(x[0])), 2) +
            result +
            pow(s.Wi(x[len(x) - 1]) - 1, 2) * (1 + pow(np.sin(2 * np.pi * s.Wi(x[len(x) - 1])), 2))
        )

    def Wi(self, x):
        return 1 + (x - 1) / 4


class Cos(BaseFunction):

    def __init__(self):
        self.Range = [-2 * np.pi, 2 * np.pi]

    def Value(s, x):
        return sum([np.cos(x) for x in x])

