from NIC_cargo.Cargo.cargo.GA import GA
from NIC_cargo.Cargo.cargo.Base.GenerateData import generate_data

car_dims = [6, 7, 6]
fname = 'NIC_cargo/new_goods.csv'

# Generate new data
generate_data(car_dims, fname)

evolution = GA(car_dims, fname=fname)
best_one = evolution.evolution()

# print(best_one.gens)
print([gen[0].index for gen in best_one.gens])
print(len(best_one.gens))
print([gen.index for gen in best_one.cargo_list])
print(len(best_one.cargo_list))

print(best_one.fitness())
