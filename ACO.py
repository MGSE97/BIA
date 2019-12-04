import matplotlib.pyplot as plt
import numpy as np
import random
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

Axes3D = Axes3D  # pycharm auto import
from Models import GraphData, Vector, Member, City
from Utils import FullFunction

NC = 20
D = 3
MIN = 0
MAX = 100

def create_city(name):
    return City(name, np.random.uniform(MIN, MAX, D-1))

def plot_aco():
  cities = [create_city(str(chr(65+x))) for x in range(0, NC)]

  fig = plt.figure('Cities ACO')
  fig.suptitle('Cities ACO')
  ax = fig.gca()
  fig.canvas.draw_idle()

  for c in cities:
      c.updateDistances(cities)
      ax.plot(c.X, c.Y, marker='v')
      ax.annotate(c.Name, (c.X - len(c.Name) / 2 - 0.25, c.Y + 2))
      print(str(c) + '\n\n')

  plt.pause(0.00001)

  while True:

      plt.pause(0.00001)

  plt.show()

