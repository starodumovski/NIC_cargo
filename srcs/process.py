# from cargo.Base.OneCargo import OneCargo #import GA
from Cargo.cargo.GA import Population, Individual
# from ..Cargo.cargo.Base.OneCargo import OneCargo
import six
# from Cargo.cargo.Base.OneCargo import OneCargo
from random import randint
from Cargo.cargo.Base.OneCargo import OneCargo

cargo_list = [OneCargo(*[randint(1, 3), randint(1, 3), randint(1, 3)]) for _ in range(5)]

a = Individual(car_length=9, car_width=9, car_height=9,
               cargo_list=cargo_list)
a.generate_individual()
print(a.cargo_list, sep='\n')
print(a.car_space)
#
# data = ['1', '2', '3', '1']
# one = OneCargo(*data)
#
# print(one.dimensions, one.weight)

# data_np = []
# for i in range(6):
#     data_tmp = [randint(1, 5), randint(1, 5), randint(1, 5), randint(4, 20)]
#     data_np.append(data_tmp)
# print(data_np)

# np.savetxt('goods.csv', data_np, delimiter=',')

# foo = np.genfromtxt('/home/starodumovski/VSProjects/NIC/project/goods.csv', delimiter=',')
# print(foo)
#
# population = Population('/home/starodumovski/VSProjects/NIC/project/goods.csv')
#
# individual = Individual(population.cargo_list)
# for i, x in enumerate(individual.cargo_list):
#     print(x.dimensions, "->", x.weight, ":", "{:.4f}".format(individual.volume_prob[i]))
# print(individual.get_cargo_sequence(use_weights=True,strict_order=True))
# print(individual.get_cargo_sequence(use_weights=True))
# print(individual.get_cargo_sequence())
# print(individual.get_cargo_sequence(strict_order=True))
#
# print("Fitness")
# print(individual.cargo_list[0].dimensions)
# # print(individual.is_fitted(individual.cargo_list[0].dimensions, {0: Dimension([0, 0, 0]), 1: Dimension([2, 5, 5])}))
# # print(individual.cargo_list[0].dimensions)
#
#
# print(individual.cargo_list[0].is_fitted({0: Dimension([0, 0, 0]), 1: Dimension([2, 1, 5])}))
#
# array = [1, 2, 3]
#
# for i in range(6):
#     tmp_arr = array[- (i//2):] + array[:- (i//2)]
#     tmp_arr = tmp_arr[0:1] + tmp_arr[1:][:: -1 if i % 2 else 1]
#     print(tmp_arr)
