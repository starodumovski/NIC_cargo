from .Base.OneCargo import OneCargo

from typing import List
from random import randint, choice

import numpy as np



class GA:
    '''
    Class of Genetic Algorithm process with initial population and their lifecycle
    '''
    def __init__(self, car_dims, fname, size_of=20, n_epochs=20) -> None:
        self.population = Population(car_dims, fname=fname, size_=size_of)
        self.size_of_population = size_of
        self.n_epochs = n_epochs

    def evolution(self):
        '''
        Lifecycle of initial population during number of epochs equals self.n_epochs 
        '''
        self.population.create_initial_population()
        for i in range(self.n_epochs):
            self.mutate()
            self.crossover()
            self.death()
        self.population.population = sorted(self.population.population, key=lambda x: -x.fitness()[0])
        return self.population.population[0]

    def mutate(self):
        '''
        Mutation of the Individual (20% that mutation will be):
            Mutation is a rotation of one of the cargo 
            in the second half of the gens sequence and 
            reloading all ones that follow the mutated one
        '''
        for individual in self.population.population:
            if np.random.choice([True, False], p=[.2, .8]):
                individual.mutate()

    def crossover(self):
        '''
        Crossover of the Individuals:
            THe crossover is reloading the individuals 
            in such a way that their crossover gens 
            must stayed at the same place if it is possible

        e.g.:                 
                              |crossover|
        parent_1:   [4, 5, 8, |  6, 3,  | 9, 1]
        parent_2:   [5, 6, 9, |  8, 4,  | 1, 3]

                              |the  same|
        child_1:    [5, 6, 3, |  8, 4,  | 9, 1]
        child_2:    [5, 9, 8, |  6, 3,  | 4, 1]
        '''
        self.population.population = sorted(self.population.population, key=lambda x: -x.fitness()[0])
        size_of_half_population = len(self.population.population) // 2
        for i in range(0, size_of_half_population, 2):
            for individual in self.population.population[i].crossover(self.population.population[i + 1]):
                self.population.population.append(individual)

    def death(self):
        '''
        kill all individual that are not so good for now
        '''
        self.population.population = sorted(
            self.population.population,
            key=lambda x: -x.fitness()[0]
        )[:self.size_of_population]


class Individual:
    '''
    We are placing all objects in such bounded 3d space:
    (a)     Z__________________________         (b) X = 6, Y = 5, Z = 3 
           /|                         /|            Bounded space:
          / |                        / |                  0  1  2  3  4 
         /  |                       /  |              0 [[3, 3, 3, 3, 3],
        /   |                      /   |              1  [3, 3, 3, 3, 3],
       /    |                     /    |              2  [3, 3, 3, 3, 3],
      /     |                    /     |              3  [3, 3, 3, 3, 3],
     /      |                   /      |              4  [3, 3, 3, 3, 3],
    /__________________________/       |              5  [3, 3, 3, 3, 3]]
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
        '''
        Load cargo in the car using the (b) notation
        '''
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
        '''
        Load the one cargo and change available space
        '''
        length = cargo.dim1
        width = cargo.dim2
        height = cargo.dim3
        for i in range(x, x + length):
            for j in range(y, y + width):
                cargo_space[i][j] -= height

        self.gens.append((cargo, x, y, cargo_space[x][y] + height))

    def find_spot(self, cargo_space, cargo):
        '''
        Find the available place for the cargo:
            If it exists, return coordinates here to load
        '''
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
        '''
        F = SUM(m_i * x_i * y_i * z_i)/car_volume * 100 + number_of_loaded_cargo/number_of_all_cargo * 100 
        '''
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
        '''
        Mutation process of an individual:
            Mutation is a rotation of one of the cargo 
            in the second half of the gens sequence and 
            reloading all ones that follow the mutated one
        '''
        index = randint(len(self.gens) // 2, len(self.gens) - 2)
        part_to_mutate = self.gens[index:]
        self.unload(part_to_mutate)
        self.gens = self.gens[:index]
        part_to_mutate = list(map(lambda cargo: cargo[0], part_to_mutate))
        part_to_mutate[0] = choice(part_to_mutate[0].get_rotations())
        self.car_space = self.packing_into_truck(part_to_mutate, self.car_space.copy())

    def crossover(self, other):
        '''
        Crossover of the Individuals:
            THe crossover is reloading the individuals 
            in such a way that their crossover gens 
            must stayed at the same place if it is possible

        e.g.:                 
                              |crossover|
        parent_1:   [4, 5, 8, |  6, 3,  | 9, 1]
        parent_2:   [5, 6, 9, |  8, 4,  | 1, 3]

                              |the  same|
        child_1:    [5, 6, 3, |  8, 4,  | 9, 1]
        child_2:    [5, 9, 8, |  6, 3,  | 4, 1]
        '''
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
        '''
        Function to unload some cargo to change the Individual
        '''
        for cargo, x, y, _ in part_to_mutate:
            for i in range(x, x + cargo.dim1):
                for j in range(y, y + cargo.dim2):
                    self.car_space[i][j] += cargo.dim3

    def generate_individual(self, weights: bool = False):
        if not weights:
            self.car_space = self.packing_into_truck(self.cargo_list.copy(), self.car_space.copy())

    def __len__(self):
        return len(self.gens)


class Population:
    '''
    Population class which will hold Individuals and keep all results
    '''
    def __init__(self, car_dims, fname: str = 'NIC_cargo/goods.csv', size_: int = 20) -> None:
        self.POPULATION_SIZE = size_
        self.cargo_list = []
        self.fname = fname
        self.create_cargo_list()
        self.car_dims = car_dims
        self.population = []

    def create_cargo_list(self):
        '''
        Retrieve list of cargo from the csv file
        '''
        for i, cargo in enumerate(np.genfromtxt(self.fname, delimiter=',')):
            self.cargo_list.append(OneCargo(*list(map(int, cargo)), index=i))
        # TODO: correct dimensions

    def create_initial_population(self):
        '''
        Create initial population by generating Individuals
        '''
        self.population = [Individual(*self.car_dims, self.cargo_list) for _ in range(self.POPULATION_SIZE)]
        for individual in self.population:
            individual.generate_individual()
        return self.population
