from Cities import plot_cities
from DifferentialEvolution import plot_diff_evolution
from Functions import Levy, Cos, Michalewicz
from Permutations import plot_permutations
from Search import plot_functions


def main():
    #plot_functions()
    #plot_cities()
    #plot_permutations()
    plot_diff_evolution(Michalewicz().SetRange(0, 4))


if __name__ == '__main__':
    main()
