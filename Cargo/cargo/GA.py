from .Base.OneCargo import OneCargo
from .Base.Dimension import Dimension
import numpy as np
from typing import List, Tuple
import six
from random import randint, choice


class GA:
    def __init__(self, car_dims, size_of=20, n_epochs=20) -> None:
        self.population = Population(car_dims, size_=size_of)
        self.size_of_population = size_of
        self.n_epochs = n_epochs

    def evolution(self):
        self.population.create_initial_population()
        for i in range(self.n_epochs):
            self.mutate()
            self.crossover()
            self.death()
        self.population.population = sorted(self.population.population, key=lambda x: -x.fitness()[0])
        return self.population.population[0]

    def mutate(self):
        for individual in self.population.population:
            if np.random.choice([True, False], p=[.2, .8]):
                individual.mutate()

    def crossover(self):
        self.population.population = sorted(self.population.population, key=lambda x: -x.fitness()[0])
        size_of_half_population = len(self.population.population) // 2
        for i in range(0, size_of_half_population, 2):
            for individual in self.population.population[i].crossover(self.population.population[i + 1]):
                self.population.population.append(individual)

    def death(self):
        self.population.population = sorted(
            self.population.population,
            key=lambda x: -x.fitness()[0]
        )[:self.size_of_population]


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
        self.car_dims = [car_length, car_width, car_height]
        self.car_volume = car_length * car_width * car_height
        self.cargo_list = [choice(cargo.get_rotations(save_init=True)) for cargo in cargo_list]
        self.cargo_list = sorted(self.cargo_list, key=lambda cargo: -cargo.get_area())
        self.gens = []

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
                if x is not None and y is not None:
                    self.put_cargo(x, y, r, car_space)
                    return self.packing_into_truck(remaining_cargos, car_space)
        return self.packing_into_truck(remaining_cargos, car_space)

    def put_cargo(self, x, y, cargo, cargo_space):
        length = cargo.dim1
        width = cargo.dim2
        height = cargo.dim3
        for i in range(x, x + length):
            for j in range(y, y + width):
                cargo_space[i][j] -= height

        self.gens.append((cargo, x, y, cargo_space[x][y] + height))

    def find_spot(self, cargo_space, cargo):
        length = cargo.dim1
        width = cargo.dim2
        height = cargo.dim3
        for i in range(len(cargo_space) - length + 1):
            for j in range(len(cargo_space[0]) - width + 1):
                is_possible = True
                z = i
                while z < length + i and is_possible:
                    k = j
                    while k < width + j and is_possible:
                        if cargo_space[z][k] - height < 0:
                            is_possible = False
                        k += 1
                    z += 1
                if is_possible:
                    return i, j
        return None, None

    def fitness(self):
        f_score = []
        f = 0
        for cargo_tuple in self.gens:
            f += cargo_tuple[0].get_volume()
        f /= self.car_volume
        f *= 100
        f_score.append(f)
        f = len(self.gens) * 100 / len(self.cargo_list)
        f_score.append(f)
        f_score.insert(0, f_score[0] + f_score[1])
        return f_score

    def mutate(self):
        index = randint(len(self.gens) // 2, len(self.gens) - 2)
        part_to_mutate = self.gens[index:]
        self.unload(part_to_mutate)
        self.gens = self.gens[:index]
        part_to_mutate = list(map(lambda cargo: cargo[0], part_to_mutate))
        part_to_mutate[0] = choice(part_to_mutate[0].get_rotations())
        self.car_space = self.packing_into_truck(part_to_mutate, self.car_space.copy())

    def crossover(self, other):
        common_len = min(len(self), len(other)) - 1
        to_cross = (max(common_len - 1, 0), common_len)
        must_have_gens_child_1 = [other.gens[i][0].index for i in to_cross]
        must_have_gens_child_2 = [self.gens[i][0].index for i in to_cross]
        sequence_child_1 = []
        sequence_child_2 = []
        for gen in self.gens:
            if gen[0].index not in must_have_gens_child_1:
                sequence_child_1.append(gen[0])
        for gen in other.gens:
            if gen[0].index not in must_have_gens_child_2:
                sequence_child_2.append(gen[0])
        for i in to_cross:
            sequence_child_1.insert(i, other.gens[i][0])
            sequence_child_2.insert(i, self.gens[i][0])
        child_1 = Individual(*self.car_dims, self.cargo_list)
        child_2 = Individual(*self.car_dims, self.cargo_list)

        child_1.car_space = child_1.packing_into_truck(sequence_child_1, child_1.car_space.copy())
        child_2.car_space = child_2.packing_into_truck(sequence_child_2, child_2.car_space.copy())

        return child_1, child_2

    def unload(self, part_to_mutate):
        for cargo, x, y, _ in part_to_mutate:
            for i in range(x, x + cargo.dim1):
                for j in range(y, y + cargo.dim2):
                    self.car_space[i][j] += cargo.dim3

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
            self.car_space = self.packing_into_truck(self.cargo_list.copy(), self.car_space.copy())

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

    def __len__(self):
        return len(self.gens)


class Population:
    def __init__(self, car_dims, fname: str = '/home/timur/University/NaturalInspiredComputing/team_task/NIC_cargo/goods.csv', size_: int = 20) -> None:
        self.POPULATION_SIZE = size_
        self.cargo_list = []
        self.fname = fname
        self.create_cargo_list()
        self.car_dims = car_dims
        self.population = []

    def create_cargo_list(self):
        for i, cargo in enumerate(np.genfromtxt(self.fname, delimiter=',')):
            self.cargo_list.append(OneCargo(*list(map(int, cargo)), index=i))
        # TODO: correct dimensions

    def create_initial_population(self):
        self.population = [Individual(*self.car_dims, self.cargo_list) for _ in range(self.POPULATION_SIZE)]
        for individual in self.population:
            individual.generate_individual()
        return self.population
