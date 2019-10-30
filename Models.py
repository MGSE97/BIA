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
