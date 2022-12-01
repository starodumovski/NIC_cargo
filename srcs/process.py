# from cargo.Base.OneCargo import OneCargo #import GA
from cargo.GA import Population, Individual
# from ..Cargo.cargo.Base.OneCargo import OneCargo
import numpy as np
from random import randint
# from Cargo.cargo.Base.OneCargo import OneCargo

from cargo.Base.OneCargo import OneCargo


data = ['1', '2', '3', '1']
one = OneCargo(*data)

print(one.measure, one.weight, one.dim_restricted)

# data_np = []
# for i in range(6):
#     data_tmp = [randint(1, 5), randint(1, 5), randint(1, 5), randint(4, 20)]
#     data_np.append(data_tmp)
# print(data_np)

# np.savetxt('goods.csv', data_np, delimiter=',')

# foo = np.genfromtxt('/home/starodumovski/VSProjects/NIC/project/goods.csv', delimiter=',')
# print(foo)

population = Population('/home/starodumovski/VSProjects/NIC/project/goods.csv')

individual = Individual(population.cargo_list)


