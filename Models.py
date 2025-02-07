import random
from copy import deepcopy

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

    def __eq__(self, o):
        x = True
        for v in self.op(o, lambda a, b: a == b).Data:
            if not v:
                x = False
                break
        return x

    def op(self, o, op):
        r = []
        if not issubclass(type(o), Vector):
            len = self.D
            for i in range(0, len):
                r.append(op(self.Data[i], o))
        else:
            len = self.D if o.D >= self.D else o.D
            for i in range(0, len):
                r.append(op(self.Data[i], o.Data[i]))

        return Vector(r)

    #def append(self, x):
     #   self.Data.append(x)
      #  self.D += 1

    def append(self, *data):
        self.Data.extend(data)
        self.D = len(data)
        return self

    def last(self):
        return self.Data[self.D-1]

    def toArray(self):
        return self.Data

    def copy(self):
        return Vector(self.Data)

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

    def append(self, *data):
        size = self.D
        super().append(data)
        if size <= 1 and len(self.Data) > 0:
            self.X = self.Data[0]
        if size <= 2 and len(self.Data) > 1:
            self.Y = self.Data[1]
        if size <= 3 and len(self.Data) > 2:
            self.Z = self.Data[2]

    def __eq__(self, o):
        return super().__eq__(o)

    def copy(self):
        return GraphData(self.Data)

class City(GraphData):
    def __init__(self, name, args):
        super().__init__(args)
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


class DistanceACO:
    def __init__(self, city, distance, visibility, pheromons):
        self.City = city
        self.Distance = distance
        self.Visibility = visibility
        self.Pheromons = pheromons

    def walk(self):
        self.Pheromons += 1.0/self.Distance
        #ant.visitedCity(self.City)


class CityACO(City):
    def updateDistances(self, cities):
        self.Distances.clear()
        for c in cities:
            if c.Name == self.Name:
                continue
            d = numpy.linalg.norm((self - c).toArray())
            self.Distances[c.Name] = DistanceACO(c, d, 1.0/d, 1)

    def getDistance(self, city):
        if city.Name == self.Name:
            return None
        return self.Distances[city.Name]


class Ant(Vector):
    def __init__(self, name, city, cities):
        self.Name = name
        self.City = city
        self.Origin = city
        self.Route = list()
        self.Route.append((city, 0.0))
        self.Distance = 0.0

    def visitedCity(self, city):
        self.City.getDistance(city).walk()
        dst = self.City.getDistance(city)
        self.Route.append((city, dst.Distance))
        self.Distance += dst.Distance
        self.City = city

    def reset(self, cities):
        self.Route.clear()
        self.Route.append((self.City, 0.0))
        self.Distance = 0.0

    def __str__(self):
        return self.Name + ' (' + str(self.Distance) + ' km) - ' + self.City.Name+ '\n\t' + \
               str.join('\n\t', [c.Name + ' (' + str(d) + ')' for c, d in self.Route])

    def str(self):
        return self.Name + ' (' + str(round(self.Distance, 2)) + ' km) ' + str.join('', [c.Name for c, d in self.Route])



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


class Member(GraphData):
    def __init__(self, args):
        super().__init__(args)
        self.Best = GraphData(self.Data)
        self.Velocity = GraphData()


class Firefly(GraphData):
    def __init__(self, args):
        super().__init__(args)

    def brightness(self):
        return self.Data[self.D-1]

    def distance(self, fly):
        return numpy.linalg.norm((self - fly).toArray())

    def __eq__(self, other):
        return super().__eq__(other)

    def copy(self):
        return Firefly(self.Data)
