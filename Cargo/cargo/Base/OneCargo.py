from .Dimension import Dimension
from itertools import permutations
import six


class OneCargo:
    def __init__(self, dim1: int, dim2: int, dim3: int, weight: float = None, dim_restricted=None) -> None:
        # try:
        #     self.dimensions = Dimension(list(map(float, [x, y, z])),
        #                                 dim_restricted if str(dim_restricted).isdigit() else None)
        # except ValueError as e:
        #     print(e, "dimensions")
        #     exit()
        #
        # self.volume = int(six.moves.reduce(lambda x, y: x * y, self.dimensions))
        #
        # try:
        #     self.weight = float(weight)
        # except ValueError as e:
        #     print(e, "weight")
        #     exit()
        # self.dim_restricted = dim_restricted if str(dim_restricted).isdigit() else None
        self.dim1, self.dim2, self.dim3 = dim1, dim2, dim3

    def get_rotations(self):
        new_cargos = list(permutations([self.dim1, self.dim2, self.dim3]))
        new_cargos.remove((self.dim1, self.dim2, self.dim3))
        return [OneCargo(*r) for r in new_cargos]

    def get_area(self):
        return self.dim1 * self.dim2

    def is_fitted(self, space_dims: dict[int, Dimension]):
        for i in self.dimensions.rotations_available:
            fitted = space_dims[0].__add__(self.dimensions.rotate(i), full=True)
            if fitted <= space_dims[1]:
                print(fitted)
                return i
        return None

    def __str__(self):
        return f'{self.dim1} x {self.dim2} x {self.dim3}, Area: {self.get_area()}'

    def __repr__(self):
        return f'{self.dim1} x {self.dim2} x {self.dim3}, Area: {self.get_area()}'
