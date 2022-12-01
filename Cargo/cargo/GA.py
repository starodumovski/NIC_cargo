from cargo.Base.OneCargo import OneCargo
import numpy as np
from typing import List

class GA:
    def __init__(self) -> None:
        pass

    def mutate():
        pass

    def crossover():
        pass


class Individual:
    def __init__(self, cargo_list_: List[OneCargo]) -> None:
        self.car_dims = [3 * 100 * 10, 1.9 * 100 * 10, 2 * 100 * 10]
        self.gens_sequence = []
        self.cargo_list: list(OneCargo) = cargo_list_
        self.weight_prob = []

    def mutate():
        pass

    def calculate_fitness_score(self):
        '''
        F(x, y, z) = (x_max - x_min) * (y_max - y_min) * (y_max - y_min)
        '''
        fitness_score = 0
        x_dim, y_dim, z_dim = 0, 0, 0
        # TODO: calculating implementation
        for element in self.gens_sequence:
            pass
        return fitness_score

    def generate_individual(self, weights: bool = False):
        pass

    def calculate_probabilities(self):
        all_mass = 0
        for cargo in self.cargo_list:
            self.weight_prob.append(cargo.weight)
            all_mass += cargo.weight
        print(self.weight_prob)
        self.weight_prob = list(map(lambda x: x/all_mass, self.weight_prob))
        print(self.weight_prob)

class Population:
    def __init__(self, fname: str, size_: int = None) -> None:
        self.POPULATION_SIZE = size_ if size_ is not None else 20
        self.car_dims = [3 * 100 * 10, 1.9 * 100 * 10, 2 * 100 * 10]
        self.population : list(Individual) | None = None
        self.cargo_list: list(OneCargo) = []
        self.fname = fname

        self.create_cargo_list()

    
    def create_cargo_list(self):
        for cargo in np.genfromtxt(self.fname, delimiter=','):
            self.cargo_list.append(OneCargo(*cargo))
        # TODO: correct dimensions

    def create_initial_population(self):
        pass