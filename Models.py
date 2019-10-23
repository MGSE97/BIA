import random

import numpy


class GraphData:
    def __init__(self, x, y, z):
        self.X = x
        self.Y = y
        self.Z = z

class Vector:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __sub__(self, o):
        return Vector(self.X - o.X, self.Y - o.Y)

    def __add__(self, o):
        return Vector(self.X + o.X, self.Y + o.Y)

    def toArray(self):
        return [self.X, self.Y]

    def __str__(self):
        return str(self.X) + ', ' + str(self.Y)

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
               str.join('\n\t', [d.Name + '(' + str(d.X) + ', ' + str(d.Y) + ') ' + str(self.Distances[d]) for d in self.Distances])

'''class CityDistance:
    def __init__(self, city, distance):
        self.City = city
        self.Distance = distance

    def __str__(self):
        return self.City.Name + '(' + str(self.City.X) + ', ' + str(self.City.Y) + ') ' + str(self.Distance)
'''
class Traveler:
    def __init__(self, name, city):
        self.Name = name
        self.City = city
        self.Origin = city
        self.Route = list()
        self.Route.append((city, 0.0))
        self.Distance = 0.0

    def __str__(self):
        return self.Name + ' (' + str(self.Distance) + ' km) - ' + self.City.Name + '(' + str(self.City.X) + ', ' + str(self.City.Y) + ')\n\t' + \
               str.join('\n\t', [c.Name + ' (' + str(d) + ')' for c, d in self.Route])

    def str(self):
        return self.Name + ' (' + str(round(self.Distance, 2)) + ' km) ' + str.join('', [c.Name for c, d in self.Route])

    def route(self, cities):
        # ToDo move to city not visited - if origin stop and return false
        path = random.sample(list(cities), k=len(cities))
        for city in path:
            if city == self.Origin:
                continue
            distance = self.City.getDistance(city)
            self.Distance += distance
            self.Route.append((city,distance))
            self.City = city

        self.Route.append((self.Origin, self.City.getDistance(self.Origin)))

