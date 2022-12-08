from .Dimension import Dimension
from itertools import permutations
import six


class OneCargo:
    def __init__(self, dim1: int, dim2: int, dim3: int, index: int, weight: float = None, dim_restricted=None) -> None:
        self.dim1, self.dim2, self.dim3 = dim1, dim2, dim3
        self.index = index

    def get_rotations(self, save_init=False):
        new_cargos = list(permutations([self.dim1, self.dim2, self.dim3]))
        if not save_init:
            new_cargos.remove((self.dim1, self.dim2, self.dim3))
        return [OneCargo(dim1=r[0], dim2=r[1], dim3=r[2], index=self.index) for r in new_cargos]

    def get_area(self):
        return self.dim1 * self.dim2

    def get_volume(self):
        return self.dim1 * self.dim2 * self.dim3

    def is_fitted(self, space_dims: dict[int, Dimension]):
        for i in self.dimensions.rotations_available:
            fitted = space_dims[0].__add__(self.dimensions.rotate(i), full=True)
            if fitted <= space_dims[1]:
                print(fitted)
                return i
        return None

    def __str__(self):
        return f'{self.dim1} x {self.dim2} x {self.dim3}, Area: {self.get_area()}, Index: {self.index}'

    def __repr__(self):
        return f'{self.dim1} x {self.dim2} x {self.dim3}, Area: {self.get_area()}, Index: {self.index}'
