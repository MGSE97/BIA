import sys

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from multiprocessing import Process

from Algorithms import BlindSearch, HillClimb
from Functions import DeSong, Ackleyr, Griewank, Rosenbrock, Rastrigin, Schwefel, Zakharov, Michalewicz, Levy, Cos
from Utils import Plot

functions = [
    DeSong(),
    Ackleyr(),#.SetRange(-5, 5),
    Griewank().SetRange(-5, 5),
    Rosenbrock().SetRange(-10, 10),
    Rastrigin(),
    Schwefel(),
    Zakharov().SetRange(-10, 10),
    Michalewicz().SetRange(0, 4),
    Levy().SetRange(-10, 10),
    Cos()
]

for i, f in enumerate(functions):
    #Plot(i+1, f, 1000, BlindSearch, 100)
    Plot(i + 1, f, 1000, HillClimb, 100)
    #plt.show()

plt.show()

#
# fig = plt.figure()
# ax = fig.gca(projection='3d')
#
# # Configure
# #function = DeSong()
# #function = Ackleyr().SetRange(-5, 5)
# #function = Griewank().SetRange(-5, 5)
# #function = Rosenbrock().SetRange(-10, 10)
# #function = Rastrigin()
# #function = Schwefel()
# #function = Zakharov().SetRange(-10, 10)
# function = Michalewicz().SetRange(0, 4)
# #function = Levy().SetRange(-10, 10)
#
# # Make data.
# search = [BlindSearch(function) for x in range(0, 100)]
# full = FullFunction(function, 1000)
#
# # Plot the surface.
# surf = ax.plot_surface(full.X, full.Y, full.Z, cmap=cm.coolwarm, linewidth=0, antialiased=True, alpha=0.5)
#
# smin = GraphData(sys.maxsize, sys.maxsize, sys.maxsize)
# smax = GraphData(-sys.maxsize, -sys.maxsize, -sys.maxsize)
# for result in search:
#     if smin.Z >= result.Z:
#         smin = result
#     if smax.Z < result.Z:
#         smax = result
#     ax.scatter(result.X, result.Y, result.Z, c="#000000")
#
# print("Minimum [", smin.X, ", ", smin.Y, "] = ", smin.Z)
# print("Maximum [", smax.X, ", ", smax.Y, "] = ", smax.Z)
#
# # Customize the z axis.
# # ax.set_zlim(data.Min, data.Max)
# ax.zaxis.set_major_locator(LinearLocator(10))
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
#
# # Add a color bar which maps values to colors.
# fig.colorbar(surf, shrink=0.5, aspect=5)
#
# plt.show()
