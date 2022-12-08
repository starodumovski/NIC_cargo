
import six
from random import randint
import numpy as np
from NIC_cargo.Cargo.cargo.Base.OneCargo import OneCargo
from NIC_cargo.Cargo.cargo.GA import GA

car_dims = [5, 7, 6]
evolution = GA(car_dims)
best_one = evolution.evolution()

print(best_one.gens)
print(len(best_one.gens))
print(best_one.cargo_list)
print(len(best_one.cargo_list))

print(best_one.fitness())


# data_np = []
# car_v = six.moves.reduce(lambda x, y: x*y, car_dims)
# while car_v > 0:
#     data_tmp = [randint(1, 3), randint(1, 3), randint(1, 3)]
#     car_v -= six.moves.reduce(lambda x, y: x*y, data_tmp)
#     data_np.append(data_tmp)
# print(data_np)
#
# np.savetxt('../goods.csv', data_np, delimiter=',')

