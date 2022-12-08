from itertools import permutations


class OneCargo:
    '''
    Class that contain the information and methods of one cargo
    '''
    def __init__(self, dim1: int, dim2: int, dim3: int, index: int, weight: float = None, dim_restricted=None) -> None:
        self.dim1, self.dim2, self.dim3 = dim1, dim2, dim3
        self.index = index

    def get_rotations(self, save_init=False):
        '''
        Rotate our object to load it in the car
        '''
        new_cargos = list(permutations([self.dim1, self.dim2, self.dim3]))
        if not save_init:
            new_cargos.remove((self.dim1, self.dim2, self.dim3))
        return [OneCargo(dim1=r[0], dim2=r[1], dim3=r[2], index=self.index) for r in new_cargos]

    def get_area(self):
        '''
        Computing the top face area
        '''
        return self.dim1 * self.dim2

    def get_volume(self):
        '''
        Computing the volume of the cargo
        '''
        return self.dim1 * self.dim2 * self.dim3

    def __str__(self):
        return f'{self.dim1} x {self.dim2} x {self.dim3}, Area: {self.get_area()}, Index: {self.index}'

    def __repr__(self):
        return f'{self.dim1} x {self.dim2} x {self.dim3}, Area: {self.get_area()}, Index: {self.index}'
