import random

import numpy


class Vector:
    def __init__(self, data=[]):
        self.Data = data
        self.D = len(data)

    def __sub__(self, o):
        return self.op(o, lambda a, b: a - b)

    def __add__(self, o):
        return self.op(o, lambda a, b: a + b)

    def __mul__(self, o):
        return self.op(o, lambda a, b: a * b)

    def __rmul__(self, o):
        return self.op(o, lambda a, b: a * b)

    def op(self, o, op):
        len = self.D if o.D >= self.D else o.D
        r = []
        for i in range(0, len):
            r.append(op(self.Data[i], o.Data[i]))

        return Vector(r)

    #def append(self, x):
     #   self.Data.append(x)
      #  self.D += 1

    def toArray(self):
        return self.Data

    def __str__(self):
        return', '.join([str(x) for x in self.Data])


class GraphData(Vector):
    def __init__(self, *args):
        super().__init__()
        self.X = 0
        self.Y = 0
        self.Z = 0
        self.set(*args)

    def set(self, *args):
        self.Data = args[0] if len(args) == 1 else args
        self.D = len(self.Data)
        if len(self.Data) > 0:
            self.X = self.Data[0]
        if len(self.Data) > 1:
            self.Y = self.Data[1]
        if len(self.Data) > 2:
            self.Z = self.Data[2]


class City(Vector):
    def __init__(self, name, x, y):
        super().__init__(x, y)
        self.Name = name
        self.Distances = {}

    def updateDistances(self, cities):
        self.Distances = dict()
        for c in cities:
            if c == self:
                continue
            self.Distances[c] = numpy.linalg.norm((self - c).toArray())

    def getDistance(self, city):
        if city == self:
            return 0.0
        return self.Distances[city]

    def __str__(self):
        return self.Name + '(' + super().__str__() + ')\n\t' + \
               str.join('\n\t', [d.Name + '(' + str(d.X) + ', ' + str(d.Y) + ') ' + str(self.Distances[d]) for d in
                                 self.Distances])


class Traveler:
    def __init__(self, name, city):
        self.Name = name
        self.City = city
        self.Origin = city
        self.Route = list()
        self.Route.append((city, 0.0))
        self.Distance = 0.0
        self.Probability = 0.0

    def __str__(self):
        return self.Name + ' (' + str(self.Distance) + ' km) - ' + self.City.Name + '(' + str(self.City.X) + ', ' + str(
            self.City.Y) + ')\n\t' + \
               str.join('\n\t', [c.Name + ' (' + str(d) + ')' for c, d in self.Route])

    def str(self):
        return self.Name + ' (' + str(round(self.Distance, 2)) + ' km) ' + str.join('', [c.Name for c, d in self.Route])

    def discover(self, cities):
        path = cities
        random.shuffle(path)
        for city in path:
            if city == self.Origin:
                continue
            distance = self.City.getDistance(city)
            self.Distance += distance
            self.Route.append((city, distance))
            self.City = city

        self.Route.append((self.Origin, self.City.getDistance(self.Origin)))

    def route(self, cities):
        self.Route.clear()
        self.Distance = 0.0
        self.Origin = cities[0]
        self.City = cities[0]
        routed = [self.City]
        self.Route.append((self.City, 0.0))
        cities.pop(0)
        cities.pop()
        for city in cities:
            if city in routed:
                for c, d in list(city.Distances.items()):
                    if c not in routed:
                        city = c
                        break
            distance = self.City.getDistance(city)
            self.Distance += distance
            self.Route.append((city, distance))
            self.City = city
            routed.append(city)

        self.Route.append((self.Origin, self.City.getDistance(self.Origin)))

    def cross(self, parent, names, ti):
        begin = random.randrange(0, len(self.Route))
        end = random.randrange(begin, len(self.Route))
        if begin == end:
            return None

        childs = [
            Traveler(
                names[random.randrange(0, len(names))] + ' ' + str(ti + 1),
                self.Origin
            ),
            Traveler(
                names[random.randrange(0, len(names))] + ' ' + str(ti + 2),
                parent.Origin
            )
        ]

        cities = [[], []]

        # Cross parents
        for i in range(0, begin):
            cities[0].append(self.Route[i][0])
            cities[1].append(parent.Route[i][0])

        for i in range(begin, end):
            cities[1].append(self.Route[i][0])
            cities[0].append(parent.Route[i][0])

        for i in range(end, len(self.Route)):
            cities[0].append(self.Route[i][0])
            cities[1].append(parent.Route[i][0])

        childs[0].route(cities[0])
        if random.randrange(0, 10) > 5:
            childs[1].route(cities[1])
        else:
            childs.remove(childs[1])

        return childs

    def mutate(self):
        a = random.randrange(0, len(self.Route))
        b = random.randrange(0, len(self.Route))
        if a == b:
            return

        cities = [c for c, d in self.Route]

        tmp = cities[a]
        cities[a] = cities[b]
        cities[b] = tmp

        self.route(cities)
