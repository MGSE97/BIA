from Cities import plot_cities
from DifferentialEvolution import plot_diff_evolution
from Functions import Levy, Cos, Michalewicz, Rastrigin
from Permutations import plot_permutations
from SOMA import plot_soma
from Search import plot_functions


def main():
    #plot_functions()
    #plot_cities()
    #plot_permutations()
    #plot_diff_evolution(Michalewicz().SetRange(0, 4))
    #plot_diff_evolution(Rastrigin())
    #plot_soma(Michalewicz().SetRange(0, 4))
    #plot_soma(Rastrigin().SetRange(0, 4))
    plot_soma(Cos())


if __name__ == '__main__':
    main()
