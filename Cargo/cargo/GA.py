from cargo.Base.OneCargo import OneCargo
import numpy as np
from typing import List
import six

class GA:
    def __init__(self) -> None:
        pass

    def mutate():
        pass

    def crossover():
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
    def __init__(self, cargo_list_: List[OneCargo]) -> None:
        self.car_dims = [3 * 100 * 10, 1.9 * 100 * 10, 2 * 100 * 10] # mm
        self.car_volume = int(six.moves.reduce(lambda x, y: x*y, self.car_dims)) # mm^3
        self.gens_sequence = []
        self.cargo_list: List[OneCargo] = cargo_list_
        self.weight_prob = []
        self.volume_prob = []

        # TODO: reduce if not needed
        self.operand = {-1 : 'move_Ox', -2 : 'move_Oy', -3 : 'move_Oz'} 

        self.calculate_probabilities()

    def mutate():
        pass

    def calculate_fitness_score(self):
        '''
        F(x, y, z) = (x_max - x_min) * (y_max - y_min) * (y_max - y_min)
        or
        F(x, y, z) = SUM(m_i * x_i * y_i * z_i)/car_volume * 100  #[percentage]
        '''
        fitness_score = 0
        x_dim, y_dim, z_dim = 0, 0, 0
        # TODO: calculating implementation
        for element in self.gens_sequence:
            pass
        return fitness_score

    # TODO: how to fill the car with considering spaces left (where to put it form start)
    def generate_individual(self, weights: bool = False):
        # TODO: generate possible individual using the numpy.choice
        order_to_load = self.get_cargo_sequence()
        pass

    def calculate_probabilities(self):
        # here it is possible to say if we have no chance to pack all
        all_weight = 0
        all_volume = 0
        for i, cargo in enumerate(self.cargo_list):
            self.weight_prob.append(cargo.weight)
            self.volume_prob.append(int(six.moves.reduce(lambda x, y: x * y, cargo.measure)))
            all_weight += cargo.weight
            all_volume += self.volume_prob[i]
        self.weight_prob = list(map(lambda x: x/all_weight, self.weight_prob))
        self.volume_prob = list(map(lambda x: x/all_volume, self.volume_prob))

    def get_cargo_sequence(self, use_weights: bool = False, strict_order: bool = False):
        if strict_order:
            if use_weights:
                cargo_prob_copy = self.weight_prob.copy()
            else:
                cargo_prob_copy = self.volume_prob.copy()
            cargo_prob_copy = {i : x for i, x in enumerate(cargo_prob_copy)}
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