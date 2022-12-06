from .Base.OneCargo import OneCargo
from .Base.Dimension import Dimension
import numpy as np
from typing import List, Tuple
import six
from random import randint


class GA:
    def __init__(self, size_of) -> None:
        pass

    def mutate(self):
        pass

    def crossover(self):
        pass


class Individual:
    '''
    We are placing all objects in such bounded 3d space:
            Z__________________________         operands:
           /|                         /|            -1 : move forward on X
          / |                        / |            -2 : move forward on Y
         /  |                       /  |            -3 : move forward on Z
        /   |                      /   |
       /    |                     /    |        All axis have magnetic effect:
      /     |                    /     |            so a point in space tends to 0
     /      |                   /      |
    /__________________________/       |
    |      *|__ __ __ __ __ __ |__ __ _|Y
    |      / (0, 0, 0)         |      /
    |     /                    |     /
    |    /                     |    /
    |   /                      |   /
    |  /                       |  /
    | /                        | /
    |/_________________________|/
    X
    '''

    def __init__(self, car_length, car_width, car_height, cargo_list: List[OneCargo]):
        self.car_space = [[car_height] * car_width for _ in range(car_length)]
        self.cargo_list = sorted(cargo_list, key=lambda cargo: -cargo.get_area())

    def packing_into_truck(self, remaining_cargos, car_space):
        if len(remaining_cargos) == 0:
            return car_space
        cargo = remaining_cargos.pop(0)
        x, y = self.find_spot(car_space, cargo)
        if x is not None and y is not None:
            self.put_cargo(x, y, cargo, car_space)
            return self.packing_into_truck(remaining_cargos, car_space)
        else:
            for r in cargo.get_rotations():
                x, y = self.find_spot(car_space, r)
                if x and y:
                    self.put_cargo(x, y, cargo, car_space)
                    return self.packing_into_truck(remaining_cargos, car_space)

    def put_cargo(self, x, y, cargo, cargo_space):
        length = cargo.dim1
        width = cargo.dim2
        height = cargo.dim3
        for i in range(x, x + length):
            for j in range(y, y + width):
                cargo_space[i][j] -= height

    def find_spot(self, cargo_space, cargo):
        length = cargo.dim1
        width = cargo.dim2
        height = cargo.dim3
        for i in range(len(cargo_space) - length):
            for j in range(len(cargo_space[0]) - width):
                is_possible = True
                z, k = i, j
                while z < length + i and is_possible:
                    while k < width + j and is_possible:
                        if cargo_space[z][k] - height < 0:
                            is_possible = False
                        k += 1
                    z += 1
                if is_possible:
                    return i, j
        return None, None

    def mutate(self):
        pass

    def calculate_fitness_score(self):
        '''
        F(x, y, z) = (x_max - x_min) * (y_max - y_min) * (y_max - y_min)
        or
        F(x, y, z) = SUM(m_i * x_i * y_i * z_i)/car_volume * 100 + number_of_loaded/number_of_all_ * 100 #[percentage]
        '''
        fitness_score = 0
        x_dim, y_dim, z_dim = 0, 0, 0
        # TODO: calculating implementation
        for element in self.gens_sequence:
            pass
        return fitness_score

    # TODO: how to fill the car with considering spaces left (where to put it form start)
    def generate_individual(self, weights: bool = False):
        if not weights:
            self.car_space = self.packing_into_truck(self.car_space.copy(), self.cargo_list)

    def calculate_probabilities(self):
        # here it is possible to say if we have no chance to pack all
        all_weight = 0
        all_volume = 0
        for i, cargo in enumerate(self.cargo_list):
            self.weight_prob.append(cargo.weight)
            self.volume_prob.append(cargo.volume)
            all_weight += cargo.weight
            all_volume += self.volume_prob[i]
        self.weight_prob = list(map(lambda x: x / all_weight, self.weight_prob))
        self.volume_prob = list(map(lambda x: x / all_volume, self.volume_prob))

    def get_cargo_sequence(self, use_weights: bool = False, strict_order: bool = False):
        if strict_order:
            if use_weights:
                cargo_prob_copy = self.weight_prob.copy()
            else:
                cargo_prob_copy = self.volume_prob.copy()
            cargo_prob_copy = {i: x for i, x in enumerate(cargo_prob_copy)}
            cargo_prob_copy = sorted(cargo_prob_copy, key=lambda x: cargo_prob_copy[x], reverse=True)
            return np.asarray([x for x in cargo_prob_copy])
        else:
            if use_weights:
                return np.random.choice(np.arange(len(self.cargo_list)),
                                        len(self.weight_prob),
                                        replace=False,
                                        p=self.weight_prob.copy())
            else:
                return np.random.choice(np.arange(len(self.cargo_list)),
                                        len(self.weight_prob),
                                        replace=False,
                                        p=self.volume_prob.copy())

        return np.random.choice()
        pass


class Population:
    def __init__(self, fname: str, size_: int = 20) -> None:
        self.POPULATION_SIZE = size_
        self.car_dims = [3 * 100 * 10, 1.9 * 100 * 10, 2 * 100 * 10]
        self.population: list(Individual) | None = None
        self.cargo_list: list(OneCargo) = []
        self.fname = fname

        self.create_cargo_list()

    def create_cargo_list(self):
        for cargo in np.genfromtxt(self.fname, delimiter=','):
            self.cargo_list.append(OneCargo(*cargo))
        # TODO: correct dimensions

    def create_initial_population(self):
        pass
