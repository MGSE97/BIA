import random
from copy import deepcopy

import matplotlib.pyplot as plt

from Models import Traveler, City

travelers = ["Horo", "Leny", "Carl", "Lawrence", "Chloe", "Nora", "Ruby", "Holo", "Gándhí", "Columbus", "Shiba", "Lucy"]
i = 0


def create_traveler(cities):
    global i
    i += 1
    traveler = Traveler(
        travelers[random.randrange(0, len(travelers))] + ' ' + str(i),
        cities[random.randrange(0, len(cities))]
    )

    traveler.discover(cities)

    return traveler


def create_population(population, cities, count):
    traveler = None
    for i in range(0, count):
        t = create_traveler(cities)
        population.append(t)
        if traveler is None or t.Distance < traveler.Distance:
            traveler = t
    return traveler


def evolve_population(population):
    global i
    # Cross
    new_population = []

    #roulette = round(random.random(), 2)
    while len(new_population) < len(population):
        t = random.sample(population, k=2)
        a = t[0]
        b = t[1]
        #if b.Probability < roulette or a.Probability < roulette:
            #roulette = round(random.random(), 2)
        c = a.cross(b, travelers, i)
        if c is not None:
            for ci, child in enumerate(c):
                if len(new_population) < len(population):
                    if child.Distance < a.Distance or child.Distance < b.Distance:
                        i += 1
                        new_population.append(child)
                    elif ci == 0:
                        new_population.append(a)
                    elif ci == 1:
                        new_population.append(b)
        else:
            new_population.append(a)
            new_population.append(b)

        if len(new_population) >= len(population):
            break
        #roulette += 0.5

    '''if len(new_population) < len(population):
        veterans = random.sample(population, k=len(population)-len(new_population)*2)
        for v in veterans:
            new_population.append(v)'''

    # Mutate
    #for m in range(0, int(len(new_population)/10)):
    new_population[random.randrange(0, len(new_population))].mutate()

    return new_population


def eval_population(population):
    best = None
    total_distance = 0.0
    # Get Best
    for traveler in population:
        if best is None or traveler.Distance < best.Distance:
            best = traveler
        #total_distance += traveler.Distance

    # Set probability to cross
    #total_distance /= len(population)

    #for traveler in population:
        #traveler.Probability = traveler.Distance / total_distance

    return best


def plot_cities():
    count = 20
    # Create cities
    cities = [City(str(chr(65+i)), random.randrange(0, 100), random.randrange(0, 100)) for i in range(0, count)]
    fig = plt.figure('Cities')
    fig.suptitle('Cities')
    ax = fig.gca()
    fig.canvas.draw_idle()

    for c in cities:
        c.updateDistances(cities)
        ax.plot(c.X, c.Y, marker='v')
        ax.annotate(c.Name, (c.X-len(c.Name)/2-0.25, c.Y+2))
        print(str(c)+'\n\n')

    plt.pause(0.00001)

    fstats = plt.figure('Travelers')
    fstats.suptitle('Best routes')
    fax = fstats.gca()
    fax.set_xlim(0, 1000)
    fax.set_ylim(0, 1200)
    fstats.canvas.draw_idle()

    distances = []
    populations = []
    current_distance = []
    max_distance = 0
    sc, = fax.plot(current_distance, populations, alpha=0.25)
    sb, = fax.plot(distances, populations)

    population = []
    t, = ax.plot([], [], alpha=0.25)
    b, = ax.plot([], [], alpha=0.5)

    # Create population
    best = deepcopy(create_population(population, cities, count*2))

    p = 0
    sp = 10
    while True:
        # Get best route from population
        traveler = eval_population(population)
        #print(traveler.str())

        if traveler.Distance > max_distance:
            max_distance = traveler.Distance
        # Update global best
        if traveler.Distance < best.Distance:
            fig.suptitle(traveler.str())
            best = deepcopy(traveler)
            plot_path(b, traveler)


        # Draw stats
        current_distance.append(traveler.Distance)
        populations.append(p)
        distances.append(best.Distance)
        if p % sp == 1:
            sb.set_xdata(populations)
            sb.set_ydata(distances)
            sc.set_xdata(populations)
            sc.set_ydata(current_distance)

            # Draw route
            plot_path(t, traveler)
            plt.pause(0.0000001)

            # Evolve population
            fax.set_xlim(0, p)
            fax.set_ylim(0, max_distance)
            if p > 1000:
                sp = 50

        population = evolve_population(population)
        p += 1

    plt.show()


def plot_path(t, traveler):
    tx = [city.X for city, distance in traveler.Route]
    ty = [city.Y for city, distance in traveler.Route]
    t.set_xdata(tx)
    t.set_ydata(ty)