import numpy as np
import six
from random import randint

def generate_data(car_dims, dest_fname='../goods.csv'):
    '''
    Generate list of cargo for the specific car dimensions to the dest_fname file
    '''
    data_np = []
    car_v = six.moves.reduce(lambda x, y: x*y, car_dims)
    while car_v > 0:
        data_tmp = [randint(1, 3), randint(1, 3), randint(1, 3)]
        car_v -= six.moves.reduce(lambda x, y: x*y, data_tmp)
        data_np.append(data_tmp)

    np.savetxt(dest_fname, data_np, delimiter=',')