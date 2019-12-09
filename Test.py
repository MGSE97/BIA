from ACO import plot_aco
from Cities import plot_cities
from DifferentialEvolution import plot_diff_evolution
from Firefly import plot_fireflies
from Functions import Levy, Cos, Michalewicz, Rastrigin, Ackleyr
from PSO import plot_pso
from Permutations import plot_permutations
from SOMA import plot_soma
from Search import plot_functions
from TLBO import plot_tlbo


def main():
    #plot_functions()
    #plot_cities()
    #plot_permutations()
    #plot_diff_evolution(Michalewicz().SetRange(0, 4))
    #plot_diff_evolution(Rastrigin())
    #plot_soma(Michalewicz().SetRange(0, 4))
    #plot_soma(Rastrigin().SetRange(0, 4))
    #plot_soma(Cos())
    #plot_pso(Michalewicz().SetRange(0, 4))
    #plot_pso(Rastrigin().SetRange(0, 4))
    #plot_pso(Cos())
    #plot_pso(Ackleyr())
    #plot_aco()
    #plot_fireflies(Rastrigin().SetRange(0, 4))
    #plot_fireflies(Ackleyr())
    plot_tlbo(Ackleyr())

if __name__ == '__main__':
    main()
