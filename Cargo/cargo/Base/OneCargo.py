
from cargo.Base.Dimension import Dimension
import six

class OneCargo:
    def __init__(self, dim_1:float, dim_2:float, dim_3:float, weight:float, dim_restricted = None) -> None:
        try:
            self.dimensions = Dimension(list(map(float, [dim_1, dim_2, dim_3])), dim_restricted if str(dim_restricted).isdigit() else None)
        except ValueError as e:
            print(e, "dimensions")
            exit()
        
        self.volume = int(six.moves.reduce(lambda x, y: x * y, self.dimensions))

        try:
            self.weight = float(weight)
        except ValueError as e:
            print(e, "weight")
            exit()
        # self.dim_restricted = dim_restricted if str(dim_restricted).isdigit() else None

    def is_fitted(self, space_dims: dict[int, Dimension]):
        for i in self.dimensions.rotations_available:
            fitted = space_dims[0].__add__(self.dimensions.rotate(i), full=True)
            if fitted <= space_dims[1]:
                print(fitted)
                return i
        return None
    


    

    